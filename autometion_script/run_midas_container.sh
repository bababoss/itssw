#!/usr/bin/env bash
var=( midas_speech-nonspeech-separation  midas_face_detection midas_nonspeech-label midas_scene_segmentation asr midas_speaker-indexing indian-language-asr midas_face_recognition )
for i in ${var[@]}
    do
        #access each element as $i. . .
        echo "Image name: ""${i}"
        id="$(docker ps -aq --filter ancestor=${i} --filter 'exited=137' --filter 'exited=0')"
        echo  "Start container id: ""${id}"
        docker start "${id}"
    done


#id="$(docker ps -aq --filter ancestor=midas_speech-nonspeech-separation --filter 'exited=137' --filter 'exited=0')"
#echo  "${id}"
