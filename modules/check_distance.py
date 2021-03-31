import app, pdb, fitbit, os, base64, json, requests
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from datetime import datetime, date, timedelta, timezone

class CheckDistanceJob:
    PIXELA_GRAPH_NAME = 'grassgraph'
    JST = timezone(timedelta(hours=+9), 'JST')

    @classmethod
    def call(cls):
        if not os.environ.get('SLACK_CHANNEL') or not os.environ.get('SLACK_BOT_TOKEN'):
            print('not setting env')
            return

        for user in app.User.query.all():
            if not user.client_id or not user.client_secret or not user.access_token or not user.refresh_token or not user.target_distance:
                continue
            
            auth2_client = fitbit.Fitbit(user.client_id, user.client_secret, oauth2=True, access_token=user.access_token, refresh_token=user.refresh_token)
            today = str((datetime.now(cls.JST)).strftime("%Y-%m-%d"))
            try:
                fit_stats_distance = auth2_client.intraday_time_series('activities/distance', base_date=today, detail_level='1min')
            except fitbit.exceptions.HTTPUnauthorized:
                cls._send_invalid_token_message_to_slack(user)
                continue
            
            kms = cls._convert_km(fit_stats_distance['activities-distance'][0]['value'])
            if cls._is_over_target_distance(kms, user.target_distance):
                cls._send_message_to_slack(user, kms)
                if not user.pixela_user_name == '' and not user.pixela_user_token == '':
                  is_success = cls._send_distance_rate_to_pixela(cls, user, kms)
                  cls._send_html_result_to_slack(cls, is_success, user)

        return 'updated!'

    def _convert_km(str_miles):
        COV_FAC = 0.621371
        kms = float(str_miles) / COV_FAC
        return round(kms, 2)
    
    def _is_over_target_distance(kms, target_distance):
        return  kms > target_distance

    def _send_invalid_token_message_to_slack(user):
        client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])
        try:            
            text = f'{user.name}さんのtokenが期限切れまたは無効になっています:man-gesturing-no:'
            client.chat_postMessage(channel=os.environ['SLACK_CHANNEL'], text=text)
        except SlackApiError as e:
            print(f"Got an error: {e.response['error']}")

    def _send_message_to_slack(user, kms):
        client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])
        try:            
            text = f'{user.name}さんが目標距離: {user.target_distance}kmを達成しました。現在の距離: {kms}km :100::woman-running::runner::man-running::skin-tone-3:'
            client.chat_postMessage(channel=os.environ['SLACK_CHANNEL'], text=text)
        except SlackApiError as e:
            print(f"Got an error: {e.response['error']}")
    
    def _check_distance_rate(kms):
        if kms <= 5.00:
            return '1'
        if 5.00 < kms and kms <= 7.50:
            return '2'
        if 7.50 < kms and kms <= 10.00:
            return '3'
        if 10.00 < kms and kms <= 12.50:
            return '4'
        if 12.50 < kms:
            return '5'
    
    def _send_distance_rate_to_pixela(cls, user, kms):
        headers = { 'X-USER-TOKEN': user.pixela_user_token }
        data = { 'date': str((datetime.now(cls.JST)).strftime("%Y%m%d")), 'quantity': cls._check_distance_rate(kms) }
        res = requests.post(f'https://pixe.la/v1/users/{user.pixela_user_name}/graphs/{cls.PIXELA_GRAPH_NAME}', headers=headers, data=json.dumps(data))
        return json.loads(res.content)['isSuccess']
    
    def _send_html_result_to_slack(cls, is_success, user):
        client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])
        text = cls._show_pixela_grass_html(cls, user) if is_success else 'グラフへの反映に失敗しました:man-gesturing-no:'
        
        try:            
            client.chat_postMessage(channel=os.environ['SLACK_CHANNEL'], text=text)
        except SlackApiError as e:
            print(f"Got an error: {e.response['error']}")

    def _show_pixela_grass_html(cls, user):
        return f'草生えるｗｗｗ\nhttps://pixe.la/v1/users/{user.pixela_user_name}/graphs/{cls.PIXELA_GRAPH_NAME}.html'

if __name__ == "__main__":
    call()
