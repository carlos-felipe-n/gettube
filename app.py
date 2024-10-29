import streamlit as st
from pytubefix import YouTube
from pytubefix.cli import on_progress
from moviepy.video.io.VideoFileClip import VideoFileClip
import os
import glob

st.header('GetTube')
#st.page_link('main.py', label='Other')
videost = st.text_input('Url')
# start = st.text_input('Tempo Inicial')
# finish = st.text_input('Tempo Final')


try:
    st.video(videost)
    name = st.text_input('Nome')
    start = st.text_input('Start Time', placeholder='HH:MM:SS')
    end = st.text_input('End time', placeholder='HH:MM:SS')

    if start != '' and end != '':

        dir = './data/'
        arquivos = glob.glob(os.path.join(dir, '*.mp4'))
        st.write('Limpando diretório...')
        for arquivo in arquivos:
            os.remove(arquivo)
            #st.write(f'Removido: {arquivo}')
        st.write('Baixando video original...')
        yt = YouTube(videost, on_progress_callback=on_progress)
        video = yt.streams.get_highest_resolution()
        video.download(output_path=dir, filename=name+'.mp4')

        st.write('Fazendo o corte do Video...')
        cut = VideoFileClip(dir+name+'.mp4',).subclip(start, end)
        output = dir+'cutted'+ name +'.mp4'
        cut.write_videofile(output, codec='libx264')

        st.write(f'Arquivo gerado com sucesso.')

        with open(output, 'rb') as video_file:
            video_bytes = video_file.read()

        st.download_button(
            label='Baixar arquivo',
            data=video_bytes,
            file_name=output,
            mime='video/mp4'
        )
    else:
        st.write('')
except:
    st.write('Aguardando video')