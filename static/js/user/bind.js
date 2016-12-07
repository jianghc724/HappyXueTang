
function submitValidation(openid) {
    if (checkUsername() & checkPassword()) {
        disableAll(true);
        showLoading(true);
        var form = document.getElementById('validationForm'),
            elems = form.elements,
            url = form.action,
            params = "openid=" + encodeURIComponent(openid),
            i, len;
        setMaxDigits(150);
        var key = new RSAKeyPair("10001","","8687cb31a720dd8712201cc4cf5ae481f7239d986b3b53673cfc5e38f468a87304af2968ee54d63acd7f90d67a52ff0d63c23a231e69477df0230a28b9db4067");
		var currentPass = document.getElementById('inputPassword').value;
        currentPass = ':' + currentPass.substr(0, 32);
        document.getElementById('inputPassword').value = encryptedString(key, currentPass);
        for (i = 0, len = elems.length; i < len; ++i) {
            params += '&' + elems[i].name + '=' + encodeURIComponent(elems[i].value);
        }
        xmlhttp = new XMLHttpRequest();
        xmlhttp.open('POST', url, true);
        xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xmlhttp.onreadystatechange = readyStateChanged;
        xmlhttp.send(params);
        document.getElementById('inputPassword').value = '';
    }
    return false;
}
