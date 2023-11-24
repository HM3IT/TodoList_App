export async function load() {

    let todos = [];

    try {
        let response = await fetch("http://localhost:8000/todos/get");

        if (! response.ok) {
            throw new Error(`HTTP error! Status: ${
                response.status
            }`);
        }

        let data = await response.json();
        todos = serilizeTodo(data);

    } catch (error) {
        console.error("Error fetching data:", error);
    }
    return {todos}
}


function serilizeTodo(data) {
    return data.map((curr) => {
        return {id: curr.id, description: curr.title, done: curr.done};
    });

}
