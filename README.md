# bluecat

This is a bluecat project that provides a cute user interface
for children to talk to the latest technology AI robot.
It can understand input in multiple languages and respond
according to the input language. This helps improve children's
communication skills and satisfy their curiosity. It can also
respond intelligently based on the child's expressions and
surrounding environment captured by the camera.
The main function:

- Multilingual Oral Communication
- Camera Function (Future)
- Animated BlueCat Feature (Future)

<img alt="img.png" src="doc/ui/chat.png" width="1282"/>

### Run the project

#### Configuration

- Python 3.11.4 (recommend)
- Node.js 20.13.1 (recommend)
- Ionic 7.2.0 (recommend)

#### Install the required packages

##### Install the required packages for the front-end project

```
cd bluecat
npm install
```

##### Install the required packages for the back-end project

```
cd bluecat_gpt
pip install -r requirements.txt
```

#### Run the back-end project in the terminal

```bash
cd bluecat_gpt/src
python main.py
```

### Run the front-end project in the terminal

```bash
cd bluecat
ionic serve
```