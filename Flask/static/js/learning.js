var player

function youtube(){
    var video_id = '{{(video_id)}}';
    player = new YT.Player("youtube", {
    width: 1600,
    height: 900,
    videoId: video_id,
});
};

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