from django.template import loader
from django.shortcuts import render
from django.http import HttpResponse
from .forms import HomeForm
import pandas as pd

from urllib.request import urlopen
import requests
import socket
import urllib.request


df = pd.read_csv('E:\DM prc\phish.csv')

df = df.head(2000)

df = df.append(df.tail(2000))

feature_column_names = ['ip_address', 'url_length', 'tiny_url', 'having_at_symbol',
       'double_slash', 'ssl_state', 'port', 'https_token', 'email_submit',
       'redirect']

predicted_class_name = ['result']

X = 0
y = 0

X = df[feature_column_names].values
y = df[predicted_class_name].values




# Create your views here.

template = loader.get_template('project/index.html')

def index(request):	

	#return render(request, 'music/index.html')
	text = ''
	msg = ''
	url_score = []
	response = 0
	t = 0
	
	if request.method == 'POST':

		form = HomeForm(request.POST)


		if form.is_valid():
			url = form.cleaned_data['post']
			form = HomeForm()


			try:
				response = (urllib.request.urlopen(url).getcode())
			except:
				msg = 'Website is not responding. Please confirm the URL is valid and try again.'

			if response != 200:
				return render(request, 'project/index.html', {'form':form, 'text':url, 'score': url_score, 'msg':msg})

			else:
				def url_length(url):
				    if len(url)>=54 and len(url)<75:
				        score1 = 0
				    elif len(url)>=75:
				        score1 = -1
				    else:
				        score1 = 1

				    url_score.append(score1)
			 


				#2
				def having_at_symbol(url):

				    score2 = 1

				    for i in url:
				        if i == '@':
				            score2 = -1
				            break

				    url_score.append(score2)
				    


				#3
				def double_slash(url):

				    score3 = 1

				    for i in range(len(url)):
				        if url[i-1] == '/' and url[i] == '/':
				            if i>7:
				                score3 = -1
				                break

				    url_score.append(score3)
				    


				#4
				def https_token(url):

				    if 'https://' in url:
				        score4 = 1
				    else:
				        score4 = -1

				    url_score.append(score4)
				    


				#5
				def ip_address(url):

				    score5 = -1
				    lenn = len(url)

				    if 'https://' in url:
				        score5 = 1
				    elif 'http://' in url:
				        for i in range(7,lenn):
				            if url[i].isalpha() == True:
				                score5 = 1
				                break
				    else:
				        score5 = -1

				    url_score.append(score5)
				    


				#6
				def tiny_url(url):

				    resp = urlopen(url)

				    score6 = 1

				    for i in url:
				        if i not in resp.url:
				            score6 = -1
				            break

				    url_score.append(score6)
				   



				#7
				def email_submit(url):

				    if 'mailto:' in url:
				        score7 = -1
				    elif 'mail()' in url:
				        score7 = -1
				    else:
				        score7 = 1

				    url_score.append(score7)
				    


				#8
				def check_ssl(url):

				    score8 = 0

				    try:
				        req = requests.get(url, verify=True)
				        score8 = 1

				    except requests.exceptions.SSLError:
				        score8 = -1


				    url_score.append(score8)
				    



				#9
				def port(url):

				    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

				    lenn = len(url)-1

				    score9 = 0

				    if (url[lenn] != '/'):
				    	url = url+'/'

				    if 'https://' in url:
				        url = url.replace('https://','')

				    elif 'http://' in url:
				        url = url.replace('http://','')


				    for i in range(lenn):
				        if url[i] == '/':
				            j = i
				            break



				    url = url[:j:]


				    #print(url)

				    result = 0
				    result1 = sock.connect_ex((url,21))
				    result2 = sock.connect_ex((url,22))
				    result3 = sock.connect_ex((url,23))
				    result4 = sock.connect_ex((url,80))
				    result5 = sock.connect_ex((url,443))
				    result6 = sock.connect_ex((url,445))
				    result7 = sock.connect_ex((url,1433))
				    result8 = sock.connect_ex((url,1521))
				    result9 = sock.connect_ex((url,3306))
				    result10 = sock.connect_ex((url,3389))

				    #result = result1+result2+result3+result4+result5+result6+result7+result8+result9+result10


				    if result1 == 0:
				       result+=1
				    if result2 == 0:
				        result+=1
				    if result3 == 0:
				        result+=1
				    if result4 == 0:
				        result+=1
				    if result5 == 0:
				        result+=1
				    if result6 == 0:
				        result+=1
				    if result7 == 0:
				        result+=1
				    if result8 == 0:
				        result+=1
				    if result9 == 0:
				        result+=1
				    if result10 == 0:
				        result+=1


				    if result>2:
				        score9 = -1
				    else:
				        score9 = 1

				    url_score.append(score9)
				    


				#10
				def redirect(url):

				    score10 = 0

				    res = urllib.request.urlopen(url)


				    finalurl = res.geturl()

				    if len(url) != len(finalurl):
				        score10 = -1
				    elif url not in finalurl:
				        score10 = -1
				    else:
				        score10 = 1

				    url_score.append(score10)

				   




				url_length(url)
				having_at_symbol(url)
				double_slash(url)
				https_token(url)
				ip_address(url)
				tiny_url(url)
				email_submit(url)
				check_ssl(url)
				port(url)
				redirect(url)

				from sklearn.ensemble import RandomForestClassifier

				# Create a RandomForestClassifier object
				rf_model = RandomForestClassifier(random_state=42)

				rf_model.fit(X, y.ravel())

				#rf_predict_train = rf_model.predict(X)

				p = rf_model.predict(url_score)


				if (p==-1 or (url_score[3]==-1 or url_score[4]==-1 or url_score[8]==-1)):
				    msg = 'This site is not safe'
				else:
				    msg = 'This site is safe'

				url_score = []

				return render(request, 'project/index.html', {'form':form, 'text':url, 'score': url_score, 'msg':msg})



	else:
		form = HomeForm()

		return render(request, 'project/index.html', {'form':form, 'text':text, 'msg':msg})


	

def result(request):

	res = 0
	msg1 = 'This site is not safe'
	msg2 = 'This site is safe'




	'''if(res>0):
		return render(request, 'music/result.html', {'msg':msg1})
	else:
		return render(request, 'music/result.html', {'msg':df.head(10)})

	'''
