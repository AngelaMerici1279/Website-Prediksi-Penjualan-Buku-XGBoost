<?php $this->load->view('headerdashboard/headerKepegawaian'); ?>
<?php $this->load->view('sidebar'); ?>
<?php $this->load->view('topbar'); ?>

<div class="container-fluid">

    <!-- Page Heading -->
    <h1 class="h3 mb-4 text-gray-800">Tambah Pegawai Baru</h1>

    <div class="row justify-content-center">
        <div class="col-xl-8 col-lg-10">
            <div class="card shadow-lg border-0 rounded-lg">
                <div class="card-header bg-primary text-white py-3">
                    <h6 class="m-0 font-weight-bold">Formulir Tambah Pegawai</h6>
                </div>
                <div class="card-body p-4">

                    <form action="<?= base_url('pegawai/insertDataPegawai'); ?>" method="post" enctype="multipart/form-data">
                        <!-- Nik -->
                        <div class="form-group mb-3">
                            <label class="font-weight-bold">NIK KTP/Nomor SIM</label>
                            <input type="text" name="nik" class="form-control" placeholder="Masukkan NIK KTP/Nomor SIM..." required>
                        </div>
                        <!-- Nama -->
                        <div class="form-group mb-3">
                            <label class="font-weight-bold">Nama Lengkap</label>
                            <input type="text" name="nama" class="form-control" placeholder="Masukkan nama lengkap..." required>
                        </div>
                        <label class="font-weight-bold">Jenis Kelamin</label><br>
                        <div class="form-check mb-3">
                            <input class="form-check-input" type="radio" name="jenis_kelamin" id="radioDefault1" value="Perempuan">
                            <label class="form-check-label" for="radioDefault1">
                                Perempuan
                            </label>
                        </div>
                        <div class="form-check">
                            <input class="form-check-input" type="radio" name="jenis_kelamin" id="radioDefault2" value="Laki-laki" checked>
                            <label class="form-check-label" for="radioDefault2">
                                Laki-laki
                            </label>
                        </div><br>
                        <!-- Password -->
                        <div class="form-group mb-3">
                            <label class="font-weight-bold">Password</label>
                            <input type="password" name="password" class="form-control" placeholder="Masukkan password..." required>
                        </div>

                        <!-- Email -->
                        <div class="form-group mb-3">
                            <label class="font-weight-bold">Email</label>
                            <input type="email" name="email" class="form-control" placeholder="contoh@email.com" required>
                        </div>

                        <!-- Alamat -->
                        <div class="form-group mb-3">
                            <label class="font-weight-bold">Alamat</label>
                            <input type="text" name="alamat" class="form-control" placeholder="Masukkan alamat..." required>
                        </div>

                        <!-- Divisi -->
                        <div class="form-group mb-3">
                            <label class="font-weight-bold">Divisi</label>
                            <select name="role_id" id="role_id" class="form-control" required>
                                <option value="">-- Pilih Divisi --</option>
                                <option value="1">Kepegawaian</option>
                                <option value="2">Penjualan</option>
                                <option value="3">Pemasaran</option>
                                <option value="4">Penerbitan</option>
                                <option value="5">Pembelian</option>
                                <option value="6">Programmer</option>
                                <option value="7">Percetakan</option>
                            </select>
                        </div>

                        <!-- Tanggal Masuk -->
                        <div class="form-group mb-3">
                            <label class="font-weight-bold">Tanggal Masuk</label>
                            <input type="date" name="tanggal_masuk" class="form-control" required>
                        </div>

                        <!-- Status -->
                        <div class="form-group mb-3">
                            <label class="font-weight-bold">Status Pegawai</label>
                            <select name="status" class="form-control" required>
                                <option value="">-- Pilih Status --</option>
                                <option value="Kontrak">Kontrak</option>
                                <option value="Tetap">Tetap</option>
                            </select>
                        </div>

                        <!-- Gaji -->
                        <div class="form-group mb-3">
                            <label class="font-weight-bold">Gaji</label>
                            <div class="input-group">
                                <span class="input-group-text">Rp</span>
                                <input type="number" name="gaji" class="form-control" placeholder="Masukkan gaji" required>
                            </div>
                        </div>

                        <!-- Upload Foto -->
                        <div class="form-group mb-3">
                            <label class="font-weight-bold">Foto Pegawai</label>
                            <input type="file" name="foto" class="form-control-file" id="fotoInput" accept="image/*">
                            <div class="mt-3 text-center">
                                <img id="previewFoto" src="https://placehold.co/120x120" alt="Preview Foto" class="img-thumbnail rounded-circle shadow-sm" style="width: 120px; height: 120px; object-fit: cover;">
                            </div>
                        </div>

                        <!-- Tombol -->
                        <div class="text-center mt-4">
                            <button type="submit" class="btn btn-primary px-4">
                                <i class="fas fa-save"></i> Simpan
                            </button>
                        </div>

                    </form>

                </div>
            </div>
        </div>
    </div>

</div>
<?php if ($this->session->flashdata('username_generate')): ?>
    <!-- Modal -->
    <div class="modal fade" id="usernameModal" tabindex="-1" role="dialog" aria-labelledby="usernameModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered" role="document">
            <div class="modal-content">
                <div class="modal-header bg-success text-white">
                    <h5 class="modal-title" id="usernameModalLabel">Pegawai Berhasil Ditambahkan 🎉</h5>
                    <button type="button" class="close text-white" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body text-center">
                    <p>Username untuk pegawai baru adalah:</p>
                    <h3 class="text-primary font-weight-bold">
                        <?= $this->session->flashdata('username_generate'); ?>
                    </h3>
                    <p class="mt-3">Simpan username ini untuk login.</p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Tutup</button>
                </div>
            </div>
        </div>
    </div>
    <!-- Pastikan jQuery dan Bootstrap JS dimuat -->
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/js/bootstrap.bundle.min.js"></script>
    
    <!-- Script untuk auto tampilkan modal -->
    <script>
        $(document).ready(function() {
            $('#usernameModal').modal('show');
        });
    </script>
<?php endif; ?>


<!-- Preview Foto JS -->
<script>
    document.getElementById('fotoInput').addEventListener('change', function(e) {
        const [file] = e.target.files;
        if (file) {
            document.getElementById('previewFoto').src = URL.createObjectURL(file);
        }
    });
</script>

<?php $this->load->view('footer'); ?>