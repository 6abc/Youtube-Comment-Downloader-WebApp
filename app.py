from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, validators
from youtube_comment_downloader import YoutubeCommentDownloader, SORT_BY_POPULAR
from itertools import islice

app = Flask(__name__)
app.config['SECRET_KEY'] = 'jaa_karle_hack_LOL'


class CommentForm(FlaskForm):
  url = StringField('Video URL',
                    validators=[validators.DataRequired(),
                                validators.URL()])
  count = IntegerField(
    'Comment Count',
    validators=[validators.DataRequired(),
                validators.NumberRange(min=1)])
  submit = SubmitField('Show Comments')


@app.route('/', methods=['GET', 'POST'])
def index():
  form = CommentForm()
  if form.validate_on_submit():
    url = form.url.data
    count = form.count.data

    downloader = YoutubeCommentDownloader()
    comments = downloader.get_comments_from_url(url, sort_by=SORT_BY_POPULAR)

    comment_list = []
    for comment in islice(comments, count):
      user = comment['author']
      comment_text = comment['text']
      user_channel = comment['channel']
      comment_list.append({
        'user':
        user,
        'comment':
        comment_text,
        'channel_url':
        f'https://www.youtube.com/channel/{user_channel}'
      })

    return render_template('comments.html', comments=comment_list)

  return render_template('index.html', form=form)


if __name__ == '__main__':
  app.run(debug=True, port='3000', host='0.0.0.0')
