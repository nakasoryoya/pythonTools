function FindProxyForURL(url, host)
{
	// Azure環境RDゲートウェイサーバ
    if(shExpMatch(host, "kcldtsgw.japanwest.cloudapp.azure.com")){
        return "PROXY oskproxy.intra.tis.co.jp:8080";
    }
    
    // googleドライブ
    if(shExpMatch(host, "*.googleapis.com")){
        return "PROXY oskproxy.intra.tis.co.jp:8080";
    }
    if(shExpMatch(host, "*.drive.ds*")){
        return "PROXY oskproxy.intra.tis.co.jp:8080";
    }
    if(shExpMatch(host, "mail.google.com")){
        return "PROXY ex-tkyproxy.intra.tis.co.jp:8080";
    }
    
    
    // slack
    if(shExpMatch(host, "files.slack.com")){
        return "PROXY ex-tkyproxy.intra.tis.co.jp:8080";
    }
    if(shExpMatch(host, "hooks.slack.com")){
        return "PROXY ex-tkyproxy.intra.tis.co.jp:8080";
    }
    
    // youtrack
    if(shExpMatch(host, "kpportal.youtrack.cloud")){
        return "PROXY ex-tkyproxy.intra.tis.co.jp:8080";
    }

    return "DIRECT";
}
