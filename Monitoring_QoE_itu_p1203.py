# Proyecto
# Por: Alejandro García Casanova
import pyshark  
import ffmpeg  
import json     
from itu_p1203 import P1203Standalone 
from itu_p1203 import extractor
import matplotlib.pyplot as plt  
from tkinter import *
from tkinter import filedialog


def box():

    root = Tk()
    root.title("Introducción de datos")
    root.geometry("630x440")
   
    var_mode = IntVar()
    var_tipo = IntVar()
    selection = ''
    
    def sel1():
        selection1 = "Seleccionado entrada de datos " + str(var_tipo.get()) 
        global tipo 
        tipo = var_tipo.get()
        print(selection1)
    def sel2():
        selection2 = "Seleccionado el modo " + str(var_mode.get())   
        global modo 
        modo = var_mode.get()
        print(selection2)
    def sel3():
        selection3 = "Pathfile: " + filepath   
        print(selection3)
        global result_box
        result_box= {'tipo':tipo,'modo':modo,'path': filepath}
        root.destroy()
    def openfile():
        global filepath
        filepath = filedialog.askopenfilename(title= 'Elegir archivo') 
    my_label1 = Label(root, text='Selecciona entrada de datos:')
    my_label1.grid(row=0, column=0, pady=20)
    tipo1 = Radiobutton(root, text ="Obtener datos de una captura de tráfico", variable=var_tipo, value=1, command=sel1)
    tipo1.grid(row=1, column=0,pady=20)
    tipo2 = Radiobutton(root, text ="Obtener datos de un archivo JSON        ", variable=var_tipo, value=2, command=sel1)
    tipo2.grid(row=2, column=0,pady=20)
    button = Button(root, text="Elegir archivo", command=openfile) 
    button.grid(row=3, column=0, pady=20)
    my_label2 = Label(root, text='Selecciona modo de funcionamiento:')
    my_label2.grid(row=0, column=3, pady=20)
    r0 = Radiobutton(root, text ="Modo de funcionamiento 0", variable=var_mode, value=0, command=sel2)
    r0.grid(row=1, column=3,pady=20)
    r1 = Radiobutton(root, text ="Modo de funcionamiento 1", variable=var_mode, value=1, command=sel2)
    r1.grid(row=2, column=3,pady=20)
    r2 = Radiobutton(root, text ="Modo de funcionamiento 2", variable=var_mode, value=2, command=sel2)
    r2.grid(row=3, column=3,pady=20)
    r3 = Radiobutton(root, text ="Modo de funcionamiento 3", variable=var_mode, value=3, command=sel2)
    r3.grid(row=4, column=3,pady=20)
    my_button = Button(root, text="Empezar", command=sel3)
    my_button.grid(row=5, column=3, pady=20)
    root.mainloop()
    return result_box





def captura_video(input, filter, length_max):

    print('')
    print('Inicio capturando paquetes de video')
    print('')

    length = 0
    video = []
    bynary_video = bytearray()
    
  

    packets = pyshark.FileCapture(
        input_file=input,
        display_filter=filter,
        use_json=True,
        include_raw=True)


    for packet in packets:  
        length += packet.__len__()  
        if (length < length_max): 
            if ("MP4" in str(packet.layers)):
                print('Paquete con protocolo mp4/video')
                video.append(str(packet.mp4_raw.value))
            elif ("MEDIA" in str(packet.layers)):
                print('Paquete con protocolo http:media/video')
                video.append(str(packet.media_raw.value))
            else:
                print('Protocolo desconocido')
        else:
            length -= packet.__len__()
    print("La tamaño de los paquetes de video es: ", length)
    for x in video:  
        bynary_video += bytearray.fromhex(x)
    f = open("video.mp4", "wb")  
    f.write(bynary_video)
    f.close


def captura_audio(input, filter, length_max):

    print('')
    print('Inicio capturando paquetes de audio')
    print('')

    length = 0
    audio = []
    bynary_audio = bytearray()

    packets = pyshark.FileCapture(
        input_file=input,
        display_filter=filter,
        use_json=True,
        include_raw=True)

    for packet in packets:  
        if ("MP4" in str(packet.layers)):
            print('Paquete con protocolo mp4/audio')
            audio.append(str(packet.mp4_raw.value))
        elif ("MEDIA" in str(packet.layers)):
            print('Paquete con protocolo http:media/audio')
            audio.append(str(packet.media_raw.value))
        else:
            print('Protocolo desconocido')

    for x in audio:  
        bynary_audio += bytearray.fromhex(x)

    f = open("audio.mp3", "wb")  
    
    f.write(bynary_audio)
    f.close


def mix_video_audio(video_file, audio_file, output_file):

    print('')
    print('Uniendo las partes de video y audio')
    print('')

    video_part = ffmpeg.input(video_file)
    audio_part = ffmpeg.input(audio_file)

    (
        ffmpeg
        
        .output(audio_part.audio,  video_part.video, output_file, shortest=None, vcodec='copy', y=None)
        .run()
    )
    


def extract_info(modo, segment):
    print('')
    print('JSON CON LA INFORMACION DEL VIDEO')
    print('')
 
    json1 = extractor.Extractor(segment, modo).extract()
    print(json.dumps(json1, indent=2))
    
    return json1

def read_json(path):

    with open(path) as f:
        json1 = json.load(f)
    return json1

def calculate_data(json_data):
    data = P1203Standalone(json_data).calculate_complete(print_intermediate=True)

    json_object = json.dumps(data, indent=2)
    print('')
    print('Resultado final:')
    print('')
    print(json_object)  
    return data


def print_plot(data):

    print('')
    print('DIBUJAMOS LAS GRÁFICAS')
    print('')
  
    d21 = data['O21']
    d22 = data['O22']
    d23 = data['O23']
    d34 = data['O34']
    d35 = data['O35']
    d46 = data['O46']
    streamid = data['streamId']
    mode = data['mode']
    date = data['date']
    seg = []
    dt = []

    for x, y in enumerate(d34):
        seg.append(str(x))

    dt.extend((d23, d35, d46))

    plt.figure(figsize=(18, 8))
    plt.suptitle('Modo:'+str(mode)+'     Fecha:' +
                str(date)+'      Identificador:'+str(streamid))

    plt.subplot(121)
    plt.title('O.23     O.35     O.46')
    bar1 = plt.bar(['Calidad de parada', 'Puntuación audiovisual general',
                    'Puntuación de calidad general'], dt)                 
    for rect in bar1:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2.0, height, '%.5f' %
                float(height), ha='center', va='bottom')

    plt.subplot(122)
    plt.title('O.34   Puntuación audiovisual general por segundo')
    bar2 = plt.bar(seg, d34)
    for rect in bar2:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2.0, height, '%.2f' %
                float(height), ha='center', va='bottom',  rotation=40)

    plt.show()



def main():

   
    result = box()
    print(result)
    if result['tipo'] == 1:

        captura_video(result['path'],'http.content_type contains "video"',9999 )
        captura_audio(result['path'],'http.content_type contains "audio"',9999 )
        mix_video_audio('video.mp4', 'audio.mp3', 'output.mp4')
        json_info = extract_info(result['modo'],["/mnt/LHDD/TFG/Codigo/output.mp4"])
        data = calculate_data(json_info)
        print_plot(data)

    elif result['tipo'] == 2:

        json_info = read_json(result['path'])
        data = calculate_data(json_info)
        print_plot(data)

    else:
        print('Introducción de datos incorrecta')
if __name__ == "__main__":
    main()