from re import split
from flask import * 
import os, demjson
app = Flask(__name__)  

CUR_DIR = os.getcwd();

# GET Homepage API
@app.route('/', methods=['POST','GET'])  
def renderHome():
    if request.method == 'GET':
        os.chdir(CUR_DIR+'/static/uploads')
        data = os.listdir()
        content = {'fileNames':[],'labels':[]}
        for index in range(0,len(data)):
            if data[index].split('.')[-1] in ['png','jpg','jpeg']:
                # print('uploads/'+data[index])
                content["fileNames"].append('uploads/'+data[index])
                try:
                    with open(CUR_DIR+'/static/bbData/'+data[index].split('.')[0]+'_frontendData.json') as file:
                        lines = file.readlines()
                        content['labels'].append(lines)
                except:
                    content['labels'].append('')
        os.chdir(CUR_DIR)
        # print(content)
        return render_template("Home.html",data=content)

# POST New image data API
@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']
        if not(f.filename in os.listdir(CUR_DIR+'/static/uploads/')):
            f.save('static/uploads/'+f.filename)
        content = getDirImages()
        return redirect("/")  

# Delete Image API
@app.route('/delete/uploads/<deviceId>', methods = ['GET'])
def deleteMedia(deviceId):
    os.chdir(CUR_DIR+'/static/uploads/')
    os.remove(deviceId)
    return redirect("/")

# Save BB List & frontend Points
@app.route('/save', methods = ['POST'])
def save():
    if request.method == 'POST':
        out_data={
            "version": "4.5.9",
            "flags": {},
            "shapes":[],
            "imagePath": "",
            "imageData": "",
            "imageHeight": None,
            "imageWidth": None
        }

        data= demjson.decode(demjson.decode(request.data)['value']);
        data= json.loads(str(data))
        # print('/n BB Details',bb_deteails)
        # Adding Data
        # print(out_data)
        out_data['name']= data[0]['name']
        out_data['imageHeight']= data[0]['imgHeight']
        out_data['imageWidtht']= data[0]['imgWidth']
        for i in range(0,len(data)):
            bb_deteails = data[i]
            print(bb_deteails)
            out_data['shapes'].append({'label':'','points':[]})
            out_data['shapes'][i]['label']= bb_deteails['label']
            for k in range(0,len(bb_deteails['pointList'])):
                point = bb_deteails['pointList'][k]
                out_data['shapes'][i]['points'].append([point['x'],point['y']])
        with open('static/imageLabels/'+bb_deteails['name'][8:].split('.')[0]+'.json','w') as f:
            f.write(json.dumps(out_data))
            f.close()
        print(out_data)
            
        print('Saveing frontend Data!!!')
        with open((CUR_DIR+'/static/bbData/'+(data[0]['name'])[8:]).split('.')[0]+'_frontendData.json', "w") as outfile:
            outfile.write(json.dumps(data))
            outfile.close()
        return jsonify({'code':200})

def getDirImages():
    os.chdir(CUR_DIR+'/static/uploads/')
    data = os.listdir()
    content = {'fileNames':[]}
    for index in range(0,len(data)):
        content["fileNames"].append(data[index])
    os.chdir(CUR_DIR)
    return content

if __name__ == '__main__':  
    app.run(debug = True)