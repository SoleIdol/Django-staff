
var show_flag = false

function show_p(wid) {
    show_flag = !show_flag
    if (show_flag) {
        // 显示评论区
        console.log('xianshi');
        $('.show_pf' + wid).attr('hidden', !show_flag)
        $('.show_pf-t' + wid).attr('hidden', false)
        $('.show_pf-f' + wid).attr('hidden', true)

    } else {
        $('.show_pf' + wid).attr('hidden', !show_flag)
        $('.show_pf-t' + wid).attr('hidden', true)
        $('.show_pf-f' + wid).attr('hidden', false)
    }

}

function reply(yuser) {
    $('input[name=m_yid]').val($(yuser).attr('yid'))
    $('input[name=m_content]').attr('placeholder', '回复' + $(yuser).attr('yname'))
}
