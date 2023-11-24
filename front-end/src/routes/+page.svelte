<script>
	import { fly, slide } from "svelte/transition";

	export let form;
	export let data;

	let inputTask = "";
	let timeoutId;

	async function inputHandler(e) {
		if (e.key != "Enter") return;

		if (inputTask != "") {
			const response = await fetch("/todoAPI", {
				method: "POST",
				body: JSON.stringify({ description: inputTask }),
				headers: {
					"Content-Type": "application/json",
				},
			});
			if (!response.ok) {
				throw new Error(`HTTP error! Status: ${response.status}`);
			}

			let { newTodo } = await response.json();
			data.todos = [...data.todos, newTodo];
			inputTask = "";
		}
	}

	async function removeTodo(id) {
		await fetch(`/todoAPI/${id}`, {
			method: "DELETE",
		});
		data.todos = data.todos.filter((cur) => cur.id != id);
	}
	async function updateTodo(todoTask) {
		const id = todoTask.id;
		await fetch(`/todoAPI/${id}`, {
			method: "PUT",
			body: JSON.stringify(todoTask),
			headers: {
				"Content-Type": "application/json",
			},
		});
	}
</script>

<section>
	<h2>TodoList App</h2>
	{#if form?.error}
		<p>{form.error}</p>
	{/if}

	<input
		type="text"
		name="description"
		id="input-textbox"
		bind:value={inputTask}
		on:keypress={inputHandler}
		required
	/>

	<ul>
		{#each data.todos as todoTask}
			<li in:fly={{ y: 20 }} out:slide={{ duration: 500 }}>
				<input
					type="text"
					class="description"
					bind:value={todoTask.description}
					on:keypress={async (e) => {
						clearTimeout(timeoutId);

						if (e.key === "Enter") {
							await updateTodo(todoTask);
						} else {
							timeoutId = setTimeout(async () => {
								await updateTodo(todoTask);
							}, 3000);
						}
					}}
				/>
				<button on:click={removeTodo(todoTask.id)}>Remove</button>
			</li>
		{/each}
	</ul>
</section>

<style>
	section {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		flex: 0.6;
	}

	li {
		list-style: none;
	}

	.description {
		display: inline-block;
		width: 300px;
		height: 1rem;
		line-height: 1rem;
		border: none;
	}
</style>
