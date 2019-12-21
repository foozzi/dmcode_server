function formatBytes(bytes, decimals = 2) {
    if (bytes === 0) return '0 Bytes';

    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];

    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}
$(document).ready(function(){
    $('#file*').click(function(){
        file_id = $(this).attr('file_id')
        $.ajax({
            url: '/fetch_file_info',
            type: 'POST',
            data: 'hash='+file_id,
            success: function(data){
                if(data.error == true){
                    //
                }
                file = data.file
                $('#file-info').hide()
                $('#file-info #link').html('<a href="/file/'+file.id+'">Open file</a>')
                $('#filesize span.value').html(formatBytes(file.filesize))
                if(file.fileext) {
                    $('#fileext').show()
                    $('#fileext span.value').html(file.fileext)
                } else {
                    $('#fileext').hide()
                }
                $('#filehash span.value').html(file.filehash)
                $('#createtime span.value').html(file.createtime)
                $('#updatetime span.value').html(file.updatetime)
                $('#fileview span.value').html(file.fileview)
                $('#file-info').show()
                $(window).scrollTop(0);
            }
        })
        return false
    })
})

