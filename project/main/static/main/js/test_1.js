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
        if (window.location.pathname.includes('/change/')) {
    
            let main_div = document.getElementById('content-main');

            let buttons_wrapper = document.createElement('div');
            buttons_wrapper.style.display = 'flex';
            buttons_wrapper.style.gap = '10px';  // расстояние между кнопками
            buttons_wrapper.style.margin = '10px 0';  // отступы сверху и снизу
            // let new_li = document.createElement('li');
            let test_send_button = document.createElement('button');
            test_send_button.textContent = 'Тестовая рассылка( в твой чат)';
            test_send_button.onclick = function() {
                let data = fetch(`http://65.108.242.208/test_send_mass_message?name_send=${name}`)
                .then(resp => {
                    resp.text().then(console.log)
                })
                alert("Тестовая рассылка запущена")
            };

            let group_send_button = document.createElement('button');
            group_send_button.textContent = 'Тестовая рассылка( в твой чат)';
            group_send_button.onclick = function() {
                let data = fetch(`http://65.108.242.208/group_send_mass_message?name_send=${name}`)
                .then(resp => {
                    resp.text().then(console.log)
                })
                alert("Рассылка в группу запущена")
            };


            let channel_send_button = document.createElement('button');
            channel_send_button.textContent = 'Тестовая рассылка( в твой чат)';
            channel_send_button.onclick = function() {
                let data = fetch(`http://65.108.242.208/chanel_send_mass_message?name_send=${name}`)
                .then(resp => {
                    resp.text().then(console.log)
                })
                alert("Рассылка в канал запущена")
            };
            


            buttons_wrapper.appendChild(test_send_button);
            buttons_wrapper.appendChild(group_send_button);
            buttons_wrapper.appendChild(channel_send_button);
            
            main_div.appendChild(buttons_wrapper)
        }
        // main_ul.append(new_li);
    }
})