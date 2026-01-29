<?php $this->load->view('headerdashboard/headerkepegawaian'); ?>
<?php $this->load->view('sidebar'); ?>
<?php $this->load->view('topbar'); ?>

<div class="container mt-5">
    <h3>Edit Data Pegawai</h3>
    <form action="<?= base_url('pegawai/updateDataPegawai'); ?>" method="post">
        <input type="hidden" name="id_pegawai" value="<?= $pegawai['id_pegawai']; ?>">

        <div class="form-group">
            <label>NIK</label>
            <input type="text" name="nik" class="form-control" value="<?= $pegawai['nik']; ?>">
        </div>

        <div class="form-group">
            <label>Nama Lengkap</label>
            <input type="text" name="nama" class="form-control" value="<?= $pegawai['nama']; ?>">
        </div>

        <div class="form-group">
            <label>Username</label>
            <input type="text" name="username" class="form-control" value="<?= $pegawai['username']; ?>">
        </div>

        <div class="form-group">
            <label>Jenis Kelamin</label>
            <select name="jenis_kelamin" class="form-control">
                <option value="Laki - laki" <?= $pegawai['jenis_kelamin'] == 'Laki - laki' ? 'selected' : ''; ?>>Laki-laki</option>
                <option value="Perempuan" <?= $pegawai['jenis_kelamin'] == 'Perempuan' ? 'selected' : ''; ?>>Perempuan</option>
            </select>
        </div>
        <div class="form-group">
            <label>Alamat</label>
            <input type="text" name="alamat" class="form-control" value="<?= $pegawai['alamat']; ?>">
        </div>

        <div class="form-group">
            <label>Email</label>
            <input type="email" name="email" class="form-control" value="<?= $pegawai['email']; ?>">
        </div>

        <div class="form-group mb-3">
            <label class="font-weight-bold">Divisi</label>
            <select name="role_id" id="role_id" class="form-control" required>
                <option value="1" <?= $pegawai['role_id'] == 1 ? 'selected' : ''; ?>>Kepegawaian</option>
                <option value="2" <?= $pegawai['role_id'] == 2 ? 'selected' : ''; ?>>Penjualan</option>
                <option value="3" <?= $pegawai['role_id'] == 3 ? 'selected' : ''; ?>>Pemasaran</option>
                <option value="4" <?= $pegawai['role_id'] == 4 ? 'selected' : ''; ?>>Penerbitan</option>
                <option value="5" <?= $pegawai['role_id'] == 5 ? 'selected' : ''; ?>>Pembelian</option>
                <option value="6" <?= $pegawai['role_id'] == 6 ? 'selected' : ''; ?>>Programmer</option>
                <option value="7" <?= $pegawai['role_id'] == 7 ? 'selected' : ''; ?>>Percetakan</option>
            </select>
        </div>


        <div class="form-group">
            <label>Tanggal Masuk</label>
            <input type="date" name="tanggal_masuk" class="form-control" value="<?= $pegawai['tanggal_masuk']; ?>">
        </div>

        <div class="form-group mb-3">
            <label class="font-weight-bold">Status Pegawai</label>
            <select name="status" id="status" class="form-control" required>
                <option value="Kontrak" <?= $pegawai['status'] == 'Kontrak' ? 'selected' : ''; ?>>Kontrak</option>
                <option value="Tetap" <?= $pegawai['status'] == 'Tetap' ? 'selected' : ''; ?>>Tetap</option>
            </select>
        </div>

        <div class="form-group">
            <label>Gaji</label>
            <input type="number" name="gaji" class="form-control" value="<?= $pegawai['gaji']; ?>">
        </div>

        <button type="submit" class="btn btn-success">Simpan Perubahan</button>
        <a href="<?= base_url('data'); ?>" class="btn btn-secondary">Kembali</a>
    </form>
</div>
<?php $this->load->view('footer'); ?>