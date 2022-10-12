var player

function input_url() {
  const input_url = document.getElementById('input').value;
    // url 타입1 - youtu.be 형식 (공유)
  if(input_url.split('/')[2] == 'youtu.be'){
    const video_id = input_url.split('/')[3]
    player = new YT.Player("youtube", {
      width: 1280,
      height: 720,
      videoId: video_id,
    });

  }
    // # url 타입2 - watch 형식 (주소창 복사)
  else if(input_url.split('?')[0] == 'https://www.youtube.com/watch'){
    const video_id = input_url.split('=')[1].split('&')[0]
    player = new YT.Player("myplayer", {
      width: 1280,
      height: 720,
      videoId: video_id,
    });
  }
}

function convert(input) {

  const afterStr = input.split(':');

  let hour = 0;
  let minutes = 0;
  let seconds = 0;

  if (afterStr.length == 3) { //시:분:초 일때
    hour = +afterStr[0]; //시
    minutes = +afterStr[1]; //분
    seconds = +afterStr[2]; //초

  } else { //분:초 일때

    minutes = +afterStr[0]; //시
    seconds = +afterStr[1]; //분

  }
  const result = hour * 3600 + minutes * 60 + seconds;

  return result;
}


$(function () {
  $(".seekTo").click(function () {
    const seektime = $(this).html();
    const seekto_s = convert(seektime);
    player.seekTo(seekto_s);
  })
})