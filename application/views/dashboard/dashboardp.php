<?php
$this->load->view('headerdashboard/headerPenjualan');
$this->load->view('sidebarPenjualan');
$this->load->view('topbar');
?>
<div class="modal fade" id="guideModal" tabindex="-1" role="dialog" aria-labelledby="guideModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered" role="document">
        <div class="modal-content">
            <div class="modal-header bg-primary text-white">
                <h5 class="modal-title font-weight-bold" id="guideModalLabel">
                    <i class="fas fa-info-circle mr-2"></i>Panduan Prediksi Penjualan
                </h5>
                <button class="close text-white" type="button" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">×</span>
                </button>
            </div>
            <div class="modal-body">
                <p>Selamat datang! Untuk melakukan prediksi penjualan tahun depan, silakan ikuti langkah berikut:</p>

                <div class="timeline-steps">
                    <div class="d-flex mb-3">
                        <div class="mr-3">
                            <span class="btn btn-circle btn-primary font-weight-bold">1</span>
                        </div>
                        <div>
                            <h6 class="font-weight-bold text-primary mb-1">Buka Menu Prediksi</h6>
                            <p class="text-gray-700 small mb-0">
                                Klik menu <b>"Penjualan"</b> di sidebar kiri, lalu pilih sub-menu <b>"Prediksi Penjualan"</b>.
                            </p>
                        </div>
                    </div>

                    <div class="d-flex mb-3">
                        <div class="mr-3">
                            <span class="btn btn-circle btn-success font-weight-bold">2</span>
                        </div>
                        <div>
                            <h6 class="font-weight-bold text-success mb-1">Input Data & Proses</h6>
                            <p class="text-gray-700 small mb-0">
                                Pilih <b>Kategori</b>, <b>Provinsi</b>, dan <b>Gudang</b> yang diinginkan, lalu klik tombol <span class="badge badge-warning">Prediksi</span>.
                            </p>
                        </div>
                    </div>

                    <div class="d-flex">
                        <div class="mr-3">
                            <span class="btn btn-circle btn-info font-weight-bold">3</span>
                        </div>
                        <div>
                            <h6 class="font-weight-bold text-info mb-1">Lihat Hasil</h6>
                            <p class="text-gray-700 small mb-0">
                                Sistem akan menampilkan tabel angka dan grafik tren penjualan untuk tahun depan.
                            </p>
                        </div>
                    </div>
                </div>

            </div>
            <div class="modal-footer">
                <button class="btn btn-secondary" type="button" data-dismiss="modal">Mengerti</button>
                <a href="<?= base_url('prediksiPenjualan'); ?>" class="btn btn-primary">
                    Coba Sekarang <i class="fas fa-arrow-right ml-1"></i>
                </a>
            </div>
        </div>
    </div>
</div>

<div class="container-fluid">

    <h1 class="h3 mb-4 text-gray-800">Dashboard Penjualan</h1>

    <div class="row">
        <div class="col-xl-3 col-md-6 mb-4">
            <div class="card border-left-primary shadow h-100 py-2 card-tahun" data-tahun="2020" style="cursor:pointer">
                <div class="card-body">
                    <div class="row no-gutters align-items-center">
                        <div class="col mr-2">
                            <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">Penjualan 2020</div>
                            <div id="total-2020" class="h5 mb-0 font-weight-bold text-gray-800">Loading...</div>
                        </div>
                        <div class="col-auto">
                            <i class="fas fa-book fa-3x text-gray-300"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>


        <div class="col-xl-3 col-md-6 mb-4">
            <div class="card border-left-primary shadow h-100 py-2 card-tahun" data-tahun="2021" style="cursor:pointer">
                <div class="card-body">
                    <div class="row no-gutters align-items-center">
                        <div class="col mr-2">
                            <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">Penjualan 2021</div>
                            <div id="total-2021" class="h5 mb-0 font-weight-bold text-gray-800">Loading...</div>
                        </div>
                        <div class="col-auto">
                            <i class="fas fa-book fa-3x text-gray-300"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="col-xl-3 col-md-6 mb-4">
            <div class="card border-left-primary shadow h-100 py-2 card-tahun" data-tahun="2022" style="cursor:pointer">
                <div class="card-body">
                    <div class="row no-gutters align-items-center">
                        <div class="col mr-2">
                            <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">Penjualan 2022</div>
                            <div id="total-2022" class="h5 mb-0 font-weight-bold text-gray-800">Loading...</div>
                        </div>
                        <div class="col-auto">
                            <i class="fas fa-book fa-3x text-gray-300"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="col-xl-3 col-md-6 mb-4">
            <div class="card border-left-primary shadow h-100 py-2 card-tahun" data-tahun="2023" style="cursor:pointer">
                <div class="card-body">
                    <div class="row no-gutters align-items-center">
                        <div class="col mr-2">
                            <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">Penjualan 2023</div>
                            <div id="total-2023" class="h5 mb-0 font-weight-bold text-gray-800">Loading...</div>
                        </div>
                        <div class="col-auto">
                            <i class="fas fa-book fa-3x text-gray-300"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="col-xl-3 col-md-6 mb-4">
            <div class="card border-left-primary shadow h-100 py-2 card-tahun" data-tahun="2024" style="cursor:pointer">
                <div class="card-body">
                    <div class="row no-gutters align-items-center">
                        <div class="col mr-2">
                            <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">Penjualan 2024</div>
                            <div id="total-2024" class="h5 mb-0 font-weight-bold text-gray-800">Loading...</div>
                        </div>
                        <div class="col-auto">
                            <i class="fas fa-book fa-3x text-gray-300"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </div>
    <div class="row" id="section-tabel-penjualan" style="display:none;">
        <div class="col-12">
            <div class="card shadow mb-4">
                <div class="card-header py-3 d-flex justify-content-between">
                    <h6 class="m-0 font-weight-bold text-primary" id="judul-tabel">Data Penjualan</h6>
                    <button class="btn btn-sm btn-danger" onclick="$('#section-tabel-penjualan').hide()">Tutup</button>
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-bordered" id="tabelDetail" width="100%" cellspacing="0">
                            <thead>
                                <tr>
                                    <th>Kategori</th>
                                    <th>Gudang</th>
                                    <th>Provinsi</th>
                                    <th>Tahun-Bulan</th>
                                    <th>Jumlah</th>
                                </tr>
                            </thead>
                            <tbody id="isi-tabel-penjualan">
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

</div>
</div>
<a class="scroll-to-top rounded" href="#page-top">
    <i class="fas fa-angle-up"></i>
</a>

<div class="modal fade" id="logoutModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel"
    aria-hidden="true">
    <div class="modal-dialog" role="document">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="exampleModalLabel">Ready to Leave?</h5>
                <button class="close" type="button" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">×</span>
                </button>
            </div>
            <div class="modal-body">Select "Logout" below if you are ready to end your current session.</div>
            <div class="modal-footer">
                <button class="btn btn-secondary" type="button" data-dismiss="modal">Cancel</button>
                <a class="btn btn-primary" href="login.html">Logout</a>
            </div>
        </div>
    </div>
</div>

<script src="<?= base_url('assets/'); ?>vendor/jquery/jquery.min.js"></script>
<script src="<?= base_url('assets/'); ?>vendor/bootstrap/js/bootstrap.bundle.min.js"></script>
<script src="<?= base_url('assets/'); ?>vendor/jquery-easing/jquery.easing.min.js"></script>
<script src="<?= base_url('assets/'); ?>js/sb-admin-2.min.js"></script>
<link href="<?= base_url('assets/'); ?>vendor/datatables/dataTables.bootstrap4.min.css" rel="stylesheet">
<script src="<?= base_url('assets/'); ?>vendor/datatables/jquery.dataTables.min.js"></script>
<script src="<?= base_url('assets/'); ?>vendor/datatables/dataTables.bootstrap4.min.js"></script>

<script>
    $(document).ready(function() {
        function formatRibuan(angka) {
            if (angka === undefined || angka === null || isNaN(angka)) return "0";
            return angka.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
        }

        $.ajax({
            url: "<?= base_url('Penjualan/getSummaryStats'); ?>",
            type: "GET",
            dataType: "json",
            success: function(response) {
                // Mengisi card otomatis berdasarkan data dari DB
                $('#total-2020').text(formatRibuan(response['2020'] || 0));
                $('#total-2021').text(formatRibuan(response['2021'] || 0));
                $('#total-2022').text(formatRibuan(response['2022'] || 0));
                $('#total-2023').text(formatRibuan(response['2023'] || 0));
                $('#total-2024').text(formatRibuan(response['2024'] || 0));
            },
            error: function(xhr) {
                console.error("Gagal mengambil data summary");
            }
        });

        $('.card-tahun').on('click', function() {
            const tahun = $(this).data('tahun');
            $('#judul-tabel').text('Detail Penjualan Tahun ' + tahun);
            $('#section-tabel-penjualan').fadeIn();

            // 1. Tampilkan loading dan Hancurkan DataTables lama jika sudah ada
            if ($.fn.DataTable.isDataTable('#tabelDetail')) {
                $('#tabelDetail').DataTable().destroy();
            }
            $('#isi-tabel-penjualan').html('<tr><td colspan="5" class="text-center">Memuat data...</td></tr>');

            $.ajax({
                url: "<?= base_url('Penjualan/getDetailByYear/'); ?>" + tahun,
                type: "GET",
                dataType: "json",
                success: function(response) {
                    let rows = '';
                    if (response.length > 0) {
                        $.each(response, function(i, item) {
                            rows += `<tr>
                        <td>${item.kategoriNama}</td>
                        <td>${item.gudangName || item.gudangNama || '-'}</td>
                        <td>${item.propNama}</td>
                        <td>${item.tahunBulan}</td>
                        <td>${formatRibuan(item.jumEks)}</td>
                    </tr>`;
                        });
                    }

                    // 2. Masukkan baris baru ke dalam tabel
                    $('#isi-tabel-penjualan').html(rows);

                    // 3. Inisialisasi DataTables untuk membuat Pagination (1 2 3 dst)
                    $('#tabelDetail').DataTable({
                        "pageLength": 10, // Menampilkan 10 data per halaman
                        "language": {
                            "url": "//cdn.datatables.net/plug-ins/1.10.24/i18n/Indonesian.json" // Opsional: Bahasa Indonesia
                        }
                    });

                    // Scroll halus ke area tabel
                    $('html, body').animate({
                        scrollTop: $("#section-tabel-penjualan").offset().top - 20
                    }, 500);
                }
            });
        });
    });
</script>
<script>
    document.addEventListener('DOMContentLoaded', function() {
        const currentLocation = window.location.href;
        const menuItems = document.querySelectorAll('.nav-link');

        menuItems.forEach(item => {
            if (item.href === currentLocation) {
                item.parentElement.classList.add('active');
            }
        });
    });
</script>

</body>

</html>