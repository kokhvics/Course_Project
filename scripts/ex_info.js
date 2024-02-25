// Функция для получения количества заданий по выбранной подтеме
function getTaskCount(subtopicName) {
    $.ajax({
        url: '/get_task_count/' + subtopicName,
        type: 'GET',
        success: function(response) {
            // Обновляем содержимое элемента с id "taskCount" значением из ответа сервера
            $('#taskCount').text(response).attr('data-task-count', response);
        },
        error: function(error) {
            console.log(error);
        }
    });
}
// Вызываем функцию получения количества заданий при загрузке страницы
var subtopicName = 'ваша_подтема_здесь';
getTaskCount(subtopicName);