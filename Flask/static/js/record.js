// 엘리먼트 취득
const $audioEl = document.querySelector("audio");
const $btn = document.getElementById("rec");

// 녹음중 상태 변수
let isRecording = false;

// MediaRecorder 변수 생성
let mediaRecorder = null;

// 녹음 데이터 저장 배열
const audioArray = [];

$btn.onclick = async function (event) {
    if(!isRecording){

        // 마이크 mediaStream 생성: Promise를 반환하므로 async/await 사용
        const mediaStream = await navigator.mediaDevices.getUserMedia({audio: true});
        
        if (navigator.mediaDevices) {
            const constraints = {
                audio: true
            }
            navigator.mediaDevices.getUserMedia(constraints)
                .then(stream => {

        // MediaRecorder 생성
        mediaRecorder = new MediaRecorder(stream);

        // 이벤트핸들러: 녹음 데이터 취득 처리
        mediaRecorder.ondataavailable = (event)=>{
            audioArray.push(event.data); // 오디오 데이터가 취득될 때마다 배열에 담아둔다.
        }

        // 이벤트핸들러: 녹음 종료 처리 & 재생하기
        mediaRecorder.onstop = (event)=>{
            
            // 녹음이 종료되면, 배열에 담긴 오디오 데이터(Blob)들을 합친다: 코덱도 설정해준다.
            const blob = new Blob(audioArray, {"type": "audio/webm"});
            audioArray.splice(0); // 기존 오디오 데이터들은 모두 비워 초기화한다.
            
            // Blob 데이터에 접근할 수 있는 주소를 생성한다.
            const blobURL = window.URL.createObjectURL(blob);

            // audio엘리먼트로 재생한다.
            $audioEl.src = blobURL;
            // $audioEl.play();

            String.prototype.format = function() {
                var formatted = this;
                for( var arg in arguments ) {
                    formatted = formatted.replace("{" + arg + "}", arguments[arg]);
                }
                return formatted;
            };
        
            let today = new Date();   
            
            function sleep(ms) {
                const wakeUpTime = Date.now() + ms;
                while (Date.now() < wakeUpTime) {}
            }

            const a = document.createElement("a")
            a.href = blobURL
            a.download = "{0}".format(today)
            a.click()
            a.remove()
            window.URL.revokeObjectURL(blobURL);

            sleep(100)

            $.ajax({
        url:'/qnaresult',
        success:function(data){
            $('#rowList').html(data);
            
        }
    })

        }

        // 녹음 시작
        mediaRecorder.start();
        $btn.innerText ='검색 종료하기 🔳 '
        $btn.style.background = "red"
        $btn.style.color = "black"
        isRecording = true;
        $('#rowList').html('');

    })
}
    }else{
        // 녹음 종료
        mediaRecorder.stop();
        $btn.innerText ='키워드 음성검색 🔘'
        $btn.style.background = "white"
        $btn.style.color = "black"
        isRecording = false;
        
    }
}