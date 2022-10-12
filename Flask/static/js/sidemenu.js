function show(classname){
  if (classname == 'videoinfo'){
      document.getElementById(classname).style.display = 'block'
      document.getElementById('videotext').style.display = 'none'
      document.getElementById('reco').style.display = 'none'
      document.getElementById('qna').style.display = 'none'

      document.getElementById('youtube').style.width ='1150px';
      document.getElementById('youtube').style.height ='650px';
      document.getElementById('mainvideotitle').style.width ='1240px';
    }
  else if(classname == 'videotext'){
    document.getElementById(classname).style.display = 'block'
    document.getElementById('videoinfo').style.display = 'none'
    document.getElementById('reco').style.display = 'none'
    document.getElementById('qna').style.display = 'none'

    document.getElementById('youtube').style.width ='1150px';
    document.getElementById('youtube').style.height ='650px';
    document.getElementById('mainvideotitle').style.width ='1240px';
  }
  else if(classname == 'reco'){
    document.getElementById(classname).style.display = 'block'
    document.getElementById('videoinfo').style.display = 'none'
    document.getElementById('videotext').style.display = 'none'
    document.getElementById('qna').style.display = 'none'

    document.getElementById('youtube').style.width ='1150px';
    document.getElementById('youtube').style.height ='650px';
    document.getElementById('mainvideotitle').style.width ='1240px';
  }
  else if(classname == 'qna'){
    document.getElementById(classname).style.display = 'block'
    document.getElementById('videoinfo').style.display = 'none'
    document.getElementById('videotext').style.display = 'none'
    document.getElementById('reco').style.display = 'none'

    document.getElementById('youtube').style.width ='1150px';
    document.getElementById('youtube').style.height ='650px';
    document.getElementById('mainvideotitle').style.width ='1240px';
  }
  }
    
function hide(classname){
  if (document.getElementById(classname).style.display = 'block'){
    document.getElementById(classname).style.display = 'none';
    document.getElementById('youtube').style.width ='1600px';
    document.getElementById('youtube').style.height ='900px';
    document.getElementById('mainvideotitle').style.width ='1690px';
}
  }

// function time(){
//   let youtube = document.getElementById('youtube');
//   youtube.innerText
    
// }