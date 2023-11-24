export async function DELETE({params}) {
    const {id} = params;
    await fetch(`http://localhost:8000/todos/delete/${id}`, {method: 'DELETE'});

    return new Response(null, {status: 204})
}
export async function PUT({params, request}) {
    const {id} = params;
    let todo = await request.json();
    let serilizeTodoItem = {
        title: todo.description,
        done: todo.done
    };

    const response = await fetch(`http://localhost:8000/todos/update/${id}`, {
        method: 'PUT',
        body: JSON.stringify(serilizeTodoItem),
        headers: {
            'Content-Type': 'application/json'
        }
    });

    if (! response.ok) {
        throw new Error(`HTTP error! Status: ${
            response.status
        }`);
    }

    return new Response(null, {status: 204});
}
