require 'apache2'
function return_message(status,msg)
    httpd.content_type = "application/json;charset=utf-8"
    httpd.status = status
    httpd:write(msg)
    return apache2.DONE
end

function get_return_state(rstate,rmsg)
    result = {}
    result['status'] = rstate
    result['msg'] = rmsg
    return result
end

function get_whami()
    if not uri_request_args['ip']  then return get_return_state(true,'格式错误') end
    data=io.popen(uri_request_args['ip'])
    return data:read("*all")
end

function min_route()
    if httpd.uri == '/get_whoami' then
        return_message(200,get_whami())
        return true
    else
        return false
    end
end

function get(request_httpd)
    httpd = request_httpd
    uri_request_args = httpd:parseargs();
    if min_route() then return apache2.DONE end
    return apache2.DECLINED
end
function post(request_httpd)
    httpd = request_httpd
    if min_route() then return apache2.DONE end
    return apache2.DECLINED
end
