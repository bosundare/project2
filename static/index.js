document.addEventListener('DOMContentLoaded', () => {
    console.log("DOM loaded.")


    room = document.querySelector("#scroll");
    room.scrollTop = 9999999;

    var socket = io.connect('http:' + '//' + document.domain + ':' + location.port);
    socket.on('connect', () => {
    console.log(document.querySelector("#sendmessage").innerHTML);
    messagesent = function() {

            const channel = document.querySelector('#current_channel').innerHTML;
            const user = document.querySelector('#current_user').innerHTML;
            const message = document.getElementById('message').value;
            socket.emit('submit message', {'channel': channel, 'message': message, 'user': user});
            document.getElementById('message').value='';
              };
    document.querySelector("#sendmessage").addEventListener("click", messagesent);
      });


      socket.on('announce message', data => {
            const li = document.createElement('li');
            channel = data.channel;
            if (channel === document.querySelector('#current_channel').innerHTML) {
                li.innerHTML = `${data.message}`;
                messages = document.querySelector("#chatroom");
                messages.append(li);

                room = document.querySelector("#scroll");
                room.scrollTop = 9999999;}
            else {
                li.innerHTML = `${channel}`;
                channels = document.querySelector("#channelslist")
                channels.append(li);
            };
          }
      );
  });
