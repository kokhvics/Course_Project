
        // Функция для извлечения параметра из URL
        function getUrlParameter(name) {
            name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
            var regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
            var results = regex.exec(location.search);
            return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
        }

        // Получаем значение параметра "subtopic" из URL
        var subtopicName = getUrlParameter('subtopic');

        // Функция для отправки запроса на получение задания по теме
        function getExerciseByTopic(topicName) {
            fetch('/get_exercises', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ topicName: topicName }),
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // Обработка полученных данных - отображаем первое задание из списка
                if (data.exercises.length > 0) {
                    // Используем функцию для отображения задания и переадресации
                    displayExerciseAndRedirect(data.exercises[0]);
                } else {
                    console.error('No exercises found for the topic:', topicName);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }
        // Пример вызова функции для получения задания по теме при загрузке страницы
            document.addEventListener('DOMContentLoaded', function() {
                getExerciseByTopic(subtopicName);
            });
             document.addEventListener('DOMContentLoaded', function() {
                // Извлекаем значение параметра из URL
                const urlParams = new URLSearchParams(window.location.search);
                const exerciseText = urlParams.get('exercise');

                // Отображаем текст задания в блоке
                const exerciseContainer = document.getElementById('exercise-container');
                exerciseContainer.textContent = exerciseText;
             });

        // Функция для отображения задания на странице и перехода к следующей странице
        function displayExerciseAndRedirect(exercise) {
            const exerciseContainer = document.getElementById('exercise-container');
            exerciseContainer.textContent = exercise; // Отображаем только одно задание

            // JavaScript для автоматического перехода через 5 секунд с передачей параметра в URL
            setTimeout(function() {
                const nextUrl = '/exersice_vars?exercise=' + encodeURIComponent(exercise); // Исправлен адрес URL
                window.location.href = nextUrl;
            }, 5000);
        }
