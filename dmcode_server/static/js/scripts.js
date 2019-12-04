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
                $('#filesize').html('File size: '+file.filesize+' kb')
                $('#fileext').html('File Extension: '+file.fileext)
                $('#filehash').html('md5: '+file.filehash)
                $('#createtime').html('File create: '+file.createtime)
                $('#updatetime').html('File last update: '+file.updatetime)
                $('#fileview').html('File views: '+file.fileview)
            }
        })
    })
})
