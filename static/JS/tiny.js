tinymce.init({
    selector: '.mytextarea',
    height: 400,
    language: 'zh_CN',
    plugins: "quickbars emoticons autoresize",       //这句话是表示插件
    inline: false,                        //这句是表示用不用内联模式
    toolbar: true,                      //工具栏关闭，选默认
    menubar: true,
    quickbars_selection_toolbar: 'bold italic | link h2 h3 blockquote',    //这句话的意思是快速工具栏可用的东西
    quickbars_insert_toolbar: 'quickimage quicktable',                         //这个开了，就可以快速插入图片，或者表格
    autoresize_max_height: 600,
    autoresize_min_height: 500,
});

