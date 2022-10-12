var videoId

function getInputURL(){
    var inputURL = document.getElementById("url").value;
    if (inputURL.split('/')[2] == 'youtu.be') {
        videoId = inputURL.split('/')[3];
    }
    else {
        videoId = inputURL.split('=')[1].split('&')[0];
    }
    
};