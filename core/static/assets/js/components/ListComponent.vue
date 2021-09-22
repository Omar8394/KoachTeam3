<template>
	<div class="d-flex flex-column justify-content-center align-items-stretch">
		<div
			class="list-group text-center"
			id="list-tab"
			role="tablist"
		>
			<a
				v-for="item in listaPaginada"
				:key="item.id"
				:class="`list-group-item list-group-item-action ${item.id == 1 ? 'active' : ''}`"
				:id="`list-${toClassCase(item.descripcion)}-list`"
				data-toggle="list"
				:href="`#list-${toClassCase(item.descripcion)}`"
				role="tab"
				:aria-controls="toClassCase(item.descripcion)"
				@click="clickedToParent({id:item.id, descripcion:item.descripcion})"
			>
				<span class="mt-1">{{ toTitleCase(item.descripcion) }}</span>
			</a>
		</div>
		<b-pagination
			class="align-self-center my-2"
			v-model="step"
			:total-rows="lista.length"
			:per-page="paginate"
		></b-pagination>
	</div>
</template>

<script>
export default {
	props: {
		//pass an array of Objects that have at least 'id' and 'descripcion' as properties
		lista: { type: Array },
		//number of element perPage
		paginate: { type: Number, default: 10 }
	},
	data() {
		return {
			step: 1
		};
	},
	methods: {
		clickedToParent: function(dataClicked) {
			this.$emit("click-element", dataClicked);
		},
		toTitleCase(name) {
			name = name.toLowerCase();
			const firstLetter = name[0].toUpperCase();
			const restOfString = name.substring(1);

			return firstLetter + restOfString;
		},
		toCamelCase(name) {
			name = name.toLowerCase();
			const words = name.split(" ").map((word, index) => {
				if (index === 0) {
					return word;
				} else {
					return this.toTitleCase(word);
				}
			});
			return words.join("");
		},
		toClassCase(name) {
			return name
				.toLowerCase()
				.split(" ")
				.join("-");
		}
	},
	computed: {
		listaPaginada: function() {
			let last = Math.ceil(this.lista.length / this.paginate);
			let listaPaginada;
			if (this.lista.length > this.paginate) {
				if (this.step === last) {
					listaPaginada = this.lista.slice(this.paginate * (last - 1));
				} else {
					listaPaginada = this.lista.slice(
						this.paginate * (this.step - 1),
						this.paginate * this.step
					);
				}
			} else {
				listaPaginada = this.lista.slice(0, this.paginate);
			}

			return listaPaginada;
		}
	}
};
</script>