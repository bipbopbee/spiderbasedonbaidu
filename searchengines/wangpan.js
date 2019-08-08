(function(){    
    var _id = 250528;
    var isHome = $('a[title="我的卡包"]').html();
    var _temp = isHome ? "" : $('span[title]:first').attr('title').slice(4);
    var _name = 'platform-tools_r22-windows.zip';
    var _path = encodeURIComponent(_temp + '/' + _name); 
    
    var _link = 'https://pcs.baidu.com/rest/2.0/pcs/file?method=download&app_id='+_id+'&path='+_path;
    alert(_link)
    console.log('%c%s','color:#00ff00;background-color:#000000;','下载地址为：\n'+_link);
})();
(function(){    
    alert('dddd')
})();
https://pcs.baidu.com/rest/2.0/pcs/file?method=download&app_id=265486&path=%2F%E6%89%8B%E6%9C%BA%E8%87%AA%E5%8A%A8%E5%8C%96.zip