window.addEventListener('load', function () {
    let is_detail_view = document.getElementsByClassName('change-form').length;
    let name = document.getElementById('id_name').value;
    console.log(name);

    // if (name) {
    //     let name_send = name.value;
    //     console.log(name_send);
    // }

    console.log(is_detail_view);
    if (is_detail_view != 0) {

        let main_div = document.getElementById('content-main');
        // let new_li = document.createElement('li');
        let mass_send_button = document.createElement('button');
        mass_send_button.textContent = 'mass_send';
        mass_send_button.onclick = function() {
            let data = fetch(`http://65.108.242.208/send_mass_message?name_send=${name}`)
            .then(resp => {
                resp.text().then(console.log)
            })
            alert("Рассылка запущена")
        };
        main_div.appendChild(mass_send_button);
        // main_ul.append(new_li);
    }
})