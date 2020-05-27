This project is hosted on http://pug-vs-bulldog-258114.appspot.com/
Make sure you use the http not https version of the site (reason explained later). The model doesn't play well with large files, try to keep them small (< 1 MB) (also explained later).

If you want to run this yourself locally:
- Bootup the Flask API with python run.py 
- Change the axios request URL in App.js to hit wherever the Flask API is hosted
- npm run local

## Brief Summary
Earlier I had built a tensorflow deep learning model that was designed to differentiate a pug from a bulldog. However, as I continued venturing into Deep Learning I realised that I could build models but never really deployed them into something I could easily show to people who asked me about my personal projects. 

As a result of this as well as the fact that I probably should gain a little exposure to front end development I decided to build a full stack web app that has a:
- ReactJS front end
- Flask REST API back end that is hooked up to my trained tensorflow model (https://github.com/Nanway/pvb_api)

The web app was designed to receive an uploaded image, calls the REST API which then passes the image through the model, receives the prediction, sends back the prediction as a JSON and then this is decoded and displayed to the user.

The frontend is deployed on Google App Engine which is serving static files. The backend is deployed from a docker container onto Google Kubernetes Engine (GKE).

## Why did you do...
I chose React as the frontend because I've always been told that you can do cool stuff with javascript as opposed to a jinja template and I thought it'd be a good idea to pickup a bit of JS. Also, I've seen a lot of job listings where knowledge of React would be beneficial and so I decided that I wanted to learn it and what better way to do so than to do a project in it.  

I chose Flask as the backend because I'm fairly familiar with it and I love the fact that it takes next to no time to get something running. Furthermore, I'm most familiar with tensorflow on python and so making the API in python would make my life far easier. 

I chose to separate the front and back ends instead of having a Flask server serve static files so that the design would be decoupled and potentially (?) mimic a full stack application better. This way it's more modular and I wouldn't have nightmares fixing problems as the front and back ends are completely separated and only linked by API calls. 

## How did you and what did you learn ...
Both the frontend and backend were deployed on the same Google Cloud platform project.

The frontend was made using create-react-app because that's the first thing I stumbled upon in the tutorials. Playing around with React was really fun and I learnt a lot about components, their lifecycles, states and how to structure them. I also expanded my CSS knowledge (through speed googling) and have thoroughly convinced myself that sometimes it is just black magic. I also learnt alot about web dev such as things like CORs, inspecting source to save my life, http vs https and uploading images/ previewing them. The frontend was built into static files that were served by Google App Engine through the NPM serve package

Doing the backend taught me a little more about how to serve a deep learning model and also gave me an experience in building a REST API since normally I would use Flask to serve websites instead of information. I also learnt how to handle form-data in Flask. The hard part was deploying the backend. Due to the CPU usage (when the model needs to be used) I had to use a cloud compute engine if I wanted to deploy this. I packaged my backend into a docker image and deployed it on Google kubernetes engine which was made to deploy docker containers. After many a tutorial, I picked up a bit about dockers, containers, exposing ports to the internet and how to deploy stuff to the cloud. The reason why the web app only works on http is because the simple setup for GKE doesn't handle https and I had enough trouble getting it out in the first place that currently I don't want to do a more advanced deployment with getting TLS keys etc etc

The model isn't very fast due to the fact that I'm using the cheapest servers so that it doesn't exceed my 1 year trial of GCP. As a result, they don't have much memory, don't have GPUs and are also located in America. Thus, predicting images can take up to 10 seconds if it's a big image - however locally it takes far less time (the bottleneck would be your CPU/GPU speed). On top of this I don't do any image compression etc etc when I upload the images which may be another reason why it takes ages.

## Big Learnings
I realised that the coding is not necessarily the hard part. In fact it was probably the easiest part to code up everything and test it locally. The big problems I ran into was when I was trying to deploy it online somewhere. I run into so many problems and so I've tried to deploy with the simplest configurations just to minimise the chances of things breaking instead of doing slightly more complex stuff such as https requests or using gunicorn instead of flask. This whole project forced me to understand all this jargon, pushed me into making decisions on which platforms to use when I barely even understood what the platforms could do and taught me a lot about the 'other side' once your app is ready to be deployed. 

In summary: this project helped me piece together some knowledge about cloud services that I will need to extend on in future.

## Future Plans
- Redesign the front end and make use of existing CSS templates better instead of trying to make my own so that it looks better
- Potentially implement a carousel of images that were recently predicted on
- Deploy the REST API with gunicorn instead of Flask
- Configure GKE to handle https requests so that I don't need to force users to use an unsecured site 
- Explore other ways of deploying AI models 
- Fine tune model (it's not too great when it gets sent an image of a bulldog that looks almost like a pug but with pointed ears)

