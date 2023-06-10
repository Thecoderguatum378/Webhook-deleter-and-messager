from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)
port = 8080

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send-message', methods=['POST'])
def send_message():
    webhook_url = request.form['webhookUrl']
    message = request.form['message']

    if webhook_url and message:
        send_message_to_discord_webhook(webhook_url, message)

    return redirect('/')

@app.route('/delete-webhook', methods=['POST'])
def delete_webhook():
    webhook_url = request.form['webhookUrlDelete']

    if webhook_url:
        delete_webhook(webhook_url)

    return redirect('/')

def send_message_to_discord_webhook(webhook_url, message):
    payload = {
        'content': message
    }

    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
        print('Message sent to Discord webhook')
    except requests.exceptions.RequestException as e:
        print('Error sending message to Discord webhook:', str(e))

def delete_webhook(webhook_url):
    try:
        response = requests.delete(webhook_url)
        if response.status_code == 204:
            print('Webhook deleted successfully.')
        else:
            print('Failed to delete webhook. Status code:', response.status_code)
    except requests.exceptions.RequestException as e:
        print('Error deleting webhook:', str(e))

if __name__ == '__main__':
    app.run(port=port)
