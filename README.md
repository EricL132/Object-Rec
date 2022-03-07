# Object Recognition 
Built with Django for backend and React for frontend, Image link/files are sent to backend to read and returns a image with boxs around objects found

# Live Demo 



# Run Locally
Run the following command in terminal to clone repo
```
git clone https://github.com/EricL132/Image-Scanner.git  
```
Create virtual environment for python so packages aren't saved globally  
Activate virtual environment
```
python -m venv env
source env/Scripts/activate
```
Install required packages (packages are listed in requirements.txt)
```
pip install -r requirements.txt
```
In readimage.py file you can either download the model once for faster boot up time or download everytime you start the program 
### To download everytime program starts leave current line
```
detector = hub.load("https://tfhub.dev/tensorflow/efficientdet/lite2/detection/1")
```
### To download once 
Download the hub from the url below and move files into hub folder located at Image-Scanner/config/utils/tensorflow/hub
```https://tfhub.dev/tensorflow/efficientdet/lite2/detection/1```  
Uncomment the line below in readimage.py and remove the above line
```
# detector = hub.KerasLayer(os.path.join(pathlib.Path(__file__).parent.absolute(),"hub"))
```
Generate secret key for django, run the following command in terminal
```
python -c "import secrets; print(secrets.token_urlsafe())"
```
Create a .env file and put secret key in there or just edit SECRET_KEY in settings.py file 
```
SECRETKEY=Generated_Key
```
Run the following command to start server, navigate to http://127.0.0.1:8000/ to see website
```
python manage.py runserver
```
# Resources
- Python
- Django
- [Tensorflow](https://www.tensorflow.org/api_docs) 