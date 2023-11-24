import {json} from '@sveltejs/kit';

export async function POST({request}) {
    try {
        const {description} = await request.json();

        let response = await fetch("http://localhost:8000/todos/add/", {
            method: 'POST',
            body: JSON.stringify(
                {title: description, done: false}
            ),
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (! response.ok) {
            throw new Error(`HTTP error! Status: ${
                response.status
            }`);
        }

        let data = await response.json();
        let newTodo = serilizeTodo(data);

        return json({
            newTodo
        }, {status: 201});

    } catch (error) {
        console.error("Error fetching data:", error);
    }
}


function serilizeTodo(data) {
    return {id: data.id, description: data.title, done: data.done};
}
