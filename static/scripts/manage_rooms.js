document.addEventListener('DOMContentLoaded', () => {
        // Connect to websocket
        var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

        // //Creat room
        // document.querySelector('#create-room').onclick = () => {
        //     const room_name = document.querySelector("#room_name").value
        //     socket.emit('create_room', {'room_name': room_name})

        //     // add row to table
        //     // // create elements
        //     // const div_row = document.createElement('div');
        //     // const div_id = document.createElement('div');
        //     // const div_name = document.createElement('div');
        //     // const div_population = document.createElement('div');
        //     // const div_btn_disable = document.createElement('div');
        //     // const btn_disable = document.createElement('button');
        //     // const div_btn_download = document.createElement('div');
        //     // const btn_download = document.createElement('button');
            
        //     // //add attributes
        //     // div_row.setAttribute('class', 'table-row');
        //     // div_id.setAttribute('class', 'table-data');
        //     // div_name.setAttribute('class', 'table-data');
        //     // div_population.setAttribute('class', 'table-data');
        //     // div_btn_disable.setAttribute('class', 'table-data');
        //     // div_btn_download.setAttribute('class', 'table-data');
        //     // btn_disable.setAttribute('class', 'disable');
        //     // btn_download.setAttribute('class', 'download-btn');
            
        //     // //add values
            
        // };
});