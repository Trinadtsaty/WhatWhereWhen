let newmessage = 0;
let open = false
document.querySelector('#unread_messages').style.display = "none"

document.querySelector('#chat_open_box').addEventListener('click', function() {
    document.querySelector('#popup_chat').classList.toggle('show');
    if (open) {
        open = false
    } else {
        open = true
        newmessage = 0;
        document.querySelector('#unread_messages').style.display = "none"
    }
//    newmessage = 0;
//    document.querySelector('#unread_messages').style.display = "none"
});



document.addEventListener('DOMContentLoaded', function() {
    const chatSocket = new WebSocket(
        'ws://' + window.location.host +
        '/ws/chat/' + room_number + '/'
    );
    // Обработчик получения сообщений
    chatSocket.onmessage = function(e) {
        if (!open) {
            document.querySelector('#unread_messages').style.display = ""
            newmessage += 1;
            document.querySelector('#unread_messages').textContent = newmessage
        }
        const data = JSON.parse(e.data);
        console.log(data);
        const chatLog = document.querySelector('#chat');
//        chatLog.innerHTML += `<div><strong>${data.username}:</strong> ${data.message}</div>`;

//        if (data.user_id === user_id) {
//            class_add = 'messege_box_my'
//
//        } else {
//            class_add = 'messege_box_not_my'
//        };

        chatLog.innerHTML +=
        `
        <div class="${data.class_add}">
            <div class="sender_box">
                <div class="sender_image"><img src="${data.picture}" alt="фото профиля" class="sender_img"></div>
                <strong class="sender_nick">${data.username}</strong>
            </div>
            <div class="text_messege">${data.message}</div>
        </div>
        `

        chatLog.scrollTop = chatLog.scrollHeight;
        console.log(newmessage)
    };

    // Обработчик отправки сообщений
    document.querySelector('#send_button').addEventListener('click', () => {
        const messageInputDom = document.querySelector('#messege');
        const message = messageInputDom.value;
        chatSocket.send(JSON.stringify({
            'room_ID': room_number,
            'message': message,
            'user_id': user_id,
        }));
        messageInputDom.value = '';
    });
    document.querySelector('#answer_button').addEventListener('click', () => {
        chatSocket.send(JSON.stringify({
            'room_ID': room_number,
            'message': "У меня есть ответ",
            'user_id': user_id,
        }));
    });


});

//messageElement.innerHTML += `<div><strong>${data.username}:</strong> ${data.message}</div>`;

document.addEventListener('DOMContentLoaded', function() {
    const chatContainer = document.getElementById('chat');

    // Прокрутка вниз при загрузке
    chatContainer.scrollTop = chatContainer.scrollHeight;

    // Если сообщения могут добавляться динамически:
    // Создаем наблюдатель за изменениями в чате
    const observer = new MutationObserver(function() {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    });


//    // Начинаем наблюдение
    observer.observe(chatContainer, {
        childList: true,  // наблюдать за добавлением/удалением детей
        subtree: true     // и всех потомков
    });
});

