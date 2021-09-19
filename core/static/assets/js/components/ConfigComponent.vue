<template>
	<!-- Listas -->
	<div>
		<b-container fluid>
			<div class="card">
				<div class="card-header">
					<div class="card-tools">
						<button
							class="btn btn-success"
							@click="newModal(descripcionPadre)"
						>
							Nuevo <i class="fas fa-plus fa-fw"></i>
						</button>
					</div>
					<p class="card-text">
						<b-row>
							<b-col
								lg="6"
								class="mt-2"
							>
								<b-form-group class="mb-0">
									<h3 class="card-title">{{ toTitleCase(descripcionAbuelo) }} - {{ toTitleCase(descripcionPadre) }}</h3>
								</b-form-group>
							</b-col>
						</b-row>
					</p>
				</div>

				<div class="card-body table-responsive p-0">
					<b-table
						:id="`tabla-${toClassCase(descripcionAbuelo)}-${toClassCase(descripcionPadre)}`"
						empty-text="No hay registros en esta tabla"
						empty-filtered-text="Ningún dato coincide con la búsqueda"
						bordered
						show-empty
						stacked="md"
						:items="hijosLista"
						:busy="isLoading"
						:fields="fields"
						:current-page="currentPage"
						:per-page="perPage"
						:filter="$parent.filter"
						:filterIncludedFields="$parent.filterOn"
						:sort-by.sync="sortBy"
						:sort-desc.sync="sortDesc"
						:sort-direction="sortDirection"
						@filtered="onFiltered"
						ref="selectableTable"
						selectable
						:select-mode="selectMode"
						@row-selected="onRowSelected"
					>
						<template #table-busy>
							<div class="text-center text-success my-2">
								<b-spinner class="align-middle"></b-spinner>
								<strong>Cargando registros...</strong>
							</div>
						</template>

						<template v-slot:cell(name)="row">
							{{ row.value.first }} {{ row.value.last }}
						</template>

						<template v-slot:cell(actions)="row">
							<b-button
								size="sm"
								href="#"
								variant="info"
								class="mr-1"
								v-b-tooltip.hover
								title="Editar"
								@click="editModal(row.item, descripcionPadre)"
							>
								<i class="fa fa-edit white"></i>
							</b-button>

							<b-button
								v-show="row.item.eliminable === 0"
								size="sm"
								variant="danger"
								class="mr-1"
								v-b-tooltip.hover
								title="Borrar"
								@click="deleteConfig(row.item.id)"
							>
								<i class="fa fa-trash"></i>
							</b-button>
						</template>
					</b-table>
				</div>
			</div>

			<b-col class="my-1">
				<b-pagination
					v-model="currentPage"
					:total-rows="totalRows"
					:per-page="perPage"
					align="right"
					size="md"
					class="my-0"
				>
				</b-pagination>
			</b-col>
		</b-container>
		<!-- Modal nuevo elemento-->
		<div
			class="modal fade"
			:id="`addNewModal${idPadre}`"
			tabindex="-1"
			role="dialog"
			:aria-labelledby="`addNewModal${idPadre}`"
			aria-hidden="true"
		>
			<div
				class="modal-dialog modal-sm modal-dialog-centered"
				role="document"
			>
				<div class="modal-content">
					<div class="modal-header dark">
						<h5 class="modal-title">
							Agregar {{ descripcionPadre }}
						</h5>
						<button
							type="button"
							class="close white"
							data-dismiss="modal"
							aria-label="Close"
						>
							<span aria-hidden="true">&times;</span>
						</button>
					</div>
					<form @submit.prevent="editmode ? updateConfig() : createConfig()">
						<div class="modal-body">
							<!-- Única fila -->
							<div class="form-row">
								<div class="form-group col-md-12">
									<div class="input-group">
										<div class="input-group-prepend">
											<span class="input-group-text"><i :class="iconoPadre"></i></span>
										</div>
										<input
											type="text"
											class="form-control"
											v-model="form.descripcion"
											:id="'elemento' + toClassCase(descripcionAbuelo) + toClassCase(descripcionPadre)"
											:placeholder="toTitleCase(descripcionPadre)"
											:aria-label="descripcionPadre"
										/>
									</div>
								</div>
							</div>
						</div>
						<div class="modal-footer">
							<button
								type="submit"
								class="btn btn-primary"
							>
								<i class="fas fa-save"></i> {{editmode? "Actualizar":"Guardar"}}
							</button>
						</div>
					</form>
				</div>
			</div>
		</div>
		<!-- fin de modal elemento -->
	</div>
	<!-- final de lista -->
</template>

<script>
export default {
	props: {
		idPadre: [String, Number],
		descripcionPadre: String,
		iconoPadre: String,
		descripcionAbuelo: String,
		cargar: Boolean
	},
	data() {
		return {
			editmode: false,
			hijosLista: [],
			isLoading: false,
			fade: false,
			form: new Form({
				id: "",
				descripcion: null,
				id_padre: this.idPadre
			}),
			fields: [
				{
					key: "descripcion",
					label: "Descripción",
					sortable: true,
					class: "text-center"
				},
				{ key: "actions", label: "Acciones", class: "text-center" }
			],
			totalRows: 1,
			currentPage: 1,
			perPage: 10,
			sortBy: "",
			sortDesc: false,
			sortDirection: "asc",
			filter: null,
			filterOn: [],
			selectMode: "multi",
			selected: []
		};
	},

	methods: {
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
		},
		reiniciarErrores() {
			this.form.clear();
			this.form.reset();
		},
		newModal(x) {
			this.reiniciarErrores();
			this.editmode = false;
			this.elemento = x;
			$("#addNewModal" + this.idPadre).modal("show");
		},
		editModal(elemento, descripcionPadre) {
			this.reiniciarErrores();
			this.elemento = descripcionPadre;
			this.editmode = true;
			this.form.id = elemento.id;
			this.form.descripcion = elemento.descripcion;
			$("#addNewModal" + this.idPadre).modal("show");
		},
		createConfig() {
			this.$Progress.start();
			this.form
				.post("api/config")
				.then(() => {
					$("#addNewModal" + this.idPadre).modal("hide");
					this.loadAll();
					this.reiniciarErrores();
				})
				.then(() => {
					Toast.fire({
						type: "success",
						title: "Configuración registrada éxitosamente"
					});
					this.$Progress.finish();
				})

				.catch(() => {
					this.$Progress.fail();
					Swal.fire({
						type: "error",
						title: "Oops...",
						text: "¡Algo ha salido mal!"
					});
				});
		},
		updateConfig() {
			this.$Progress.start();
			this.form
				.put(`api/config/${this.form.id}`)
				.then(() => {
					$("#addNewModal" + this.idPadre).modal("hide");
					this.loadAll();
					this.reiniciarErrores();
				})
				.then(() => {
					Toast.fire({
						type: "success",
						title: "Configuración actualizada éxitosamente"
					});
					this.$Progress.finish();
				})

				.catch(() => {
					this.$Progress.fail();
					Swal.fire({
						type: "error",
						title: "Oops...",
						text: "¡Algo ha salido mal!"
					});
				});
		},
		deleteConfig(id) {
			Swal.fire({
				title: "¿Está seguro?",
				text:
					"¡No podrá revertir los cambios, al eliminar una configuración en uso se borraran los registros donde este presente!",
				type: "warning",
				showCancelButton: true,
				confirmButtonColor: "#3085d6",
				cancelButtonColor: "#d33",
				confirmButtonText: "¡Sí, eliminar!"
			}).then(result => {
				//Enviar solicitud para borrar al servidor
				if (result.value) {
					this.form
						.delete("api/config/" + id)
						.then(() => {
							this.loadAll();
							Swal.fire(
								"¡Eliminado!",
								"La configuración ha sido eliminada",
								"success"
							);
						})
						.catch(() => {
							Swal.fire({
								type: "error",
								title: "Oops...",
								text: "¡Algo ha salido mal!"
							});
						});
				}
			});
		},
		onRowSelected(items) {
			this.selected = items;
		},

		onFiltered(filteredItems) {
			// Trigger pagination to update the number of buttons/pages due to filtering
			this.totalRows = filteredItems.length;
			this.currentPage = 1;
		},

		async loadAll() {
			this.isLoading = true;
			const hijosApi = await axios.get(`api/configHijo/${this.idPadre}`);
			this.hijosLista = await hijosApi.data;
			this.isLoading = false;
		}
	},
	computed: {
		cargarHijos: function() {
			if (this.cargar) {
				this.loadAll();
			} else {
				this.limpiar();
			}
		}
	},
	created() {
		this.loadAll();
		Fire.$on("AfterCreate", () => {
			this.loadAll();
		});
	}
};
</script>
