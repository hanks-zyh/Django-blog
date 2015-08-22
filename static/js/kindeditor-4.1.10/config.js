/**
 * Created by Administrator on 2015/8/22.
 */
KindEditor.ready(function(K) {
	K.create('textarea[name="content"]', {
		width : "1000px",
    	        height : "400px",
		uploadJson: '/admin/uploads/kindeditor',
	});
});