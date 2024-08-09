# FLASK APP FOR FUNNY TWEET ANNOTATIONS TASK #

from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import csv

# load in data
df = pd.read_csv("./data/all_tweets.csv")
done_df = pd.read_csv("./data/funny-annotations.csv")
done_array = list(done_df['id'])

# initialize flask app
app = Flask(__name__)
app.secret_key = 'supersecretkey'  # needed to use sessions

@app.route('/', methods=['GET', 'POST'])
def index():
    # initiate sesion variables
    if 'tweet_index' not in session:
        session['tweet_index'] = 0
    tweet_index = session['tweet_index']
    if 'annotations' not in session:
        session['annotations'] = []

    # get tweets that are not yet annotated
    while (df['id'][tweet_index] in done_array):
        tweet_index += 1
        session['tweet_index'] = tweet_index

    if (request.method == 'POST'): 
        # get annotated answer
        annotation = request.form.get('annotation')

        # add answer to session array
        if annotation:
            an_item = {'id': str(df['id'][tweet_index]), 'funny': annotation}
            session['annotations'].append(an_item)
            tweet_index += 1
            session['tweet_index'] = tweet_index
            
    # save answer (i have anxiety about deleting everything by accident)
    if session['annotations'] != []:
        save_annotations(session['annotations'])

    # show tweet
    current_tweet = df['tweets'][tweet_index].replace('\n', '<br>')
    current_id = df['id'][tweet_index]

    return render_template('index.html', tweet=current_tweet, id=current_id)

@app.route('/reset_session')
def reset_session():
    session.clear()  
    return redirect(url_for('index'))  

# save annotations progress
def save_annotations(annotations):
    with open('./data/funny-annotations.csv', 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['id', 'funny'])
        # for annotation in annotations:
        writer.writerow(annotations[-1])

if __name__ == '__main__':
    app.run(debug=True,  host='127.0.0.1')