let myImage = document.querySelector('img');
var imgList = ['logo3.png','lol.jpeg','3.png'];
var imgIdx = 1;  //默认数值当前index


//切换图片事件。
myImage.onclick = function(){
    /*
    let mySrc = myImage.getAttribute('src');
    if(mySrc = 'lol.jpeg'){
        myImage.setAttribute('src','logo3.png');
    }else{
        myImage.setAttribute('src','lol.jpeg');
    }
    */
    let mySrc = myImage.getAttribute('src');
    myImage.setAttribute('src',imgList[imgIdx]);
    imgIdx >= (imgList.length - 1) ? imgIdx = 0 : imgIdx++;
}

let myButton = document.querySelector('button');
let myHadding = document.querySelector('h1')
//创建输入姓名函数，并创建元素name。
function setUserName() {
    let myName = prompt('请输入你的名字');
    if (! myName  || myName === null) {
        setUserName();
    } else {
        localStorage.setItem('name',myName);
        myHadding.textContent = 'Mozilla 酷毙了，' + myName;
    }
}


//判断name是否存在，如果不存在执行函数。
if (! localStorage.getItem('name')) {
    setUserName();
} else {
    let storedName = localStorage.getItem('name');
    myHadding.textContent = 'Mozilla 酷毙了，' + storedName;
}

//添加事件，运行添加姓名事件。
myButton.onclick = function(){
    setUserName();
}



