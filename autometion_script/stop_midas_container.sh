var=( midas_speech-nonspeech-separation  midas_face_detection midas_nonspeech-label midas_scene_segmentation )
for i in ${var[@]}
    do
        #access each element as $i. . .
        echo  "Docker Image: ""${i}"
        id="$(docker ps -aq --filter ancestor=${i} --filter status=running)"
        echo  "Stop container id: ""${id}"
        docker stop "${id}"
    done
#id="$(docker ps -aq --filter ancestor=midas_speech-nonspeech-separation --filter 'exited=137' --filter 'exited=0')"
#echo  "${id}"
