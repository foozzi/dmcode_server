$(document).ready(function(){
    $('#file*').click(function(){
        file_id = $(this).attr('file_id')
        $.ajax({
            url: '/fetch_file_info',
            type: 'POST',
            data: 'id='+file_id,
            success: function(data){
                if(data.error == true){
                    //
                }
                file = data.file
                $('#file-info').hide()
                $('#file-info #link').html('<a href="/file/'+file.id+'">Open file</a>')
                $('#filesize span.value').html(file.filesize)
                $('#fileext span.value').html(file.fileext)
                $('#filehash span.value').html(file.filehash)
                $('#createtime span.value').html(file.createtime)
                $('#updatetime span.value').html(file.updatetime)
                $('#fileview span.value').html(file.fileview)
                $('#file-info').show()
            }
        })
        return false
    })

    $('pre.content code').each(function(i, block) {
        hljs.lineNumbersBlock(block);
    });
})
