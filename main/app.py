import requests
import os
from datetime import datetime
import json

API_KEY = os.getenv('API_KEY', 'AIzaSyAVZhXNtFnRkq0Dzx8WZLTd4hxRo-w98q4')

def lambda_handler(event, context):
    http_method = event['httpMethod']
    path = event['path']

    if http_method == 'POST' and path == '/get_video_details':
        try:
            body = json.loads(event['body'])
            video_url = body['video_url']
            video_id = extract_video_id(video_url)
            if video_id:
                video_details = fetch_video_details(video_id, API_KEY)
                if video_details:
                    return {
                        'statusCode': 200,
                        'body': json.dumps({'video_details': video_details}),
                        'headers': {'Content-Type': 'application/json'}
                    }
                else:
                    return {
                        'statusCode': 400,
                        'body': json.dumps({'message': 'Failed to fetch video details'}),
                        'headers': {'Content-Type': 'application/json'}
                    }
            else:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'message': 'Invalid YouTube video URL. Please try again.'}),
                    'headers': {'Content-Type': 'application/json'}
                }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'message': str(e)}),
                'headers': {'Content-Type': 'application/json'}
            }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({'message': 'Not Found'}),
            'headers': {'Content-Type': 'application/json'}
        }

def extract_video_id(video_url):
    if 'youtube.com' in video_url or 'youtu.be' in video_url:
        if 'youtube.com' in video_url:
            video_id = video_url.split('v=')[1]
        else:
            video_id = video_url.split('/')[-1]
        return video_id
    else:
        return None

def fetch_video_details(video_id, api_key):
    url = f'https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={api_key}'
    response = requests.get(url)
    video_data = response.json()
    if 'items' in video_data and len(video_data['items']) > 0:
        snippet = video_data['items'][0]['snippet']
        publish_time = snippet['publishedAt']
        title = snippet['title']
        description = snippet['description']
        return {
            'title': title,
            'description': description,
            'publish_time': datetime.strptime(publish_time, '%Y-%m-%dT%H:%M:%SZ').strftime('%m/%d/%Y')
        }
    else:
        return None

if __name__ == '__main__':
    event = {
        'httpMethod': 'POST',
        'path': '/get_video_details',
        'body': json.dumps({'video_url': 'https://www.youtube.com/watch?v=8D0ZqJ3c_jc'})
    }
    context = {}
    print(lambda_handler(event, context))