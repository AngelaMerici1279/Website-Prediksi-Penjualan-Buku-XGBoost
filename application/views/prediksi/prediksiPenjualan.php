<?php
$this->load->view('headerdashboard/headerPenjualan');
$this->load->view('sidebarPenjualan');
$this->load->view('topbar');
?>

<div class="container-fluid">

    <h1 class="h3 mb-4 text-gray-800">Prediksi Penjualan Buku</h1>

    <div class="card shadow mb-4">
        <div class="card-body">
            <form id="formPrediksi">
                <div class="row">
                    <div class="col-md-4">
                        <div class="form-group">
                            <label for="dropdownKategori" class="font-weight-bold">Pilih Kategori</label>
                            <select class="form-control" id="dropdownKategori" name="kategori">
                                <option value="">-- Pilih Kategori --</option>
                                <?php foreach ($kategori as $kat): ?>
                                    <option value="<?= $kat; ?>"><?= $kat; ?></option>
                                <?php endforeach; ?>
                            </select>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="form-group">
                            <label for="dropdownProvinsi" class="font-weight-bold">Pilih Provinsi</label>
                            <select class="form-control" id="dropdownProvinsi" name="provinsi">
                                <option value="">-- Pilih Provinsi --</option>
                                <?php foreach ($provinsi as $prov): ?>
                                    <option value="<?= $prov; ?>"><?= $prov; ?></option>
                                <?php endforeach; ?>
                            </select>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="form-group">
                            <label for="dropdownGudang" class="font-weight-bold">Pilih Gudang</label>
                            <select class="form-control" id="dropdownGudang" name="gudang">
                                <option value="">-- Pilih Gudang --</option>
                                <?php foreach ($gudang as $g): ?>
                                    <option value="<?= $g; ?>"><?= $g; ?></option>
                                <?php endforeach; ?>
                            </select>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="form-group">
                            <label for="pilihBulan" class="font-weight-bold">Bulan Prediksi (2025)</label>
                            <select class="form-control border-left-primary" id="pilihBulan" name="bulan_target">
                                <option value="1">Januari</option>
                                <option value="2">Februari</option>
                                <option value="3">Maret</option>
                                <option value="4">April</option>
                                <option value="5">Mei</option>
                                <option value="6">Juni</option>
                                <option value="7">Juli</option>
                                <option value="8">Agustus</option>
                                <option value="9">September</option>
                                <option value="10">Oktober</option>
                                <option value="11">November</option>
                                <option value="12">Desember</option>
                            </select>
                        </div>
                    </div>
                </div>
                <div class="mt-3 text-center">
                    <button type="button" id="btnPrediksi" class="btn btn-warning">
                        <i class="fa-solid fa-chart-line"></i> Prediksi
                    </button>
                </div>
            </form>
        </div>
    </div>

    <!-- TABEL HASIL -->
    <div class="card shadow mb-4" id="cardHasil" style="display:none;">
        <div class="card-header py-3">
            <h6 class="m-0 font-weight-bold text-warning">Hasil Prediksi</h6>
        </div>
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-bordered" id="tabelPrediksi" width="100%" cellspacing="0">
                    <thead class="thead-light">
                        <tr>
                            <th>Kategori</th>
                            <th class="text-center">Bulan Target</th>
                            <th class="text-right bg-warning text-white">Hasil Prediksi</th>
                            <th class="text-right bg-danger text-white">MAE (Error)</th>
                            <th class="text-right bg-primary text-white">Error (%)</th>
                            <th class="text-center bg-info text-white">Rekomendasi Stok (Rentang)</th>
                        </tr>
                    </thead>
                    <tbody></tbody>
                </table>
            </div>
            <div class="text-right mt-3">
                <button type="button" id="btnSimpan" class="btn btn-success">
                    <i class="fa-solid fa-save"></i> Simpan Hasil Prediksi
                </button>
            </div>
        </div>
    </div>

    <!-- GRAFIK -->
    <div class="card shadow mb-4" id="cardGrafik" style="display:none;">
        <div class="card-header py-3">
            <h6 class="m-0 font-weight-bold text-info">Visualisasi Tren: Historis vs Prediksi</h6>
        </div>
        <div class="card-body">
            <div class="chart-area" style="height: 400px;">
                <canvas id="chartPrediksi"></canvas>
            </div>
            <hr>
            <div class="text-center small">
                <span class="mr-2"><i class="fas fa-circle text-secondary"></i> Data Historis</span>
                <span class="mr-2"><i class="fas fa-circle text-warning"></i> Prediksi ML</span>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

</div>
</div>
<?php $this->load->view('footer'); ?>
</div>
<script>
    let salesChart = null;

    $('#btnPrediksi').click(function() {
        var kategori = $('#dropdownKategori').val();
        var provinsi = $('#dropdownProvinsi').val();
        var gudang = $('#dropdownGudang').val();
        var bulanInput = $('#pilihBulan').val();

        if (!kategori || !provinsi || !gudang) {
            Swal.fire({
                icon: 'warning',
                title: 'Data Belum Lengkap',
                text: 'Harap pilih semua opsi!'
            });
            return;
        }

        Swal.fire({
            title: 'Sedang Menghitung...',
            text: 'Mohon tunggu...',
            allowOutsideClick: false,
            didOpen: () => {
                Swal.showLoading();
            }
        });

        $.ajax({
            url: "<?= base_url('penjualan/hitungPrediksi'); ?>",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({
                kategori: kategori,
                provinsi: provinsi,
                gudang: gudang
            }),
            dataType: "json",
            success: function(response) {
                Swal.close();

                if (!response.forecast || response.forecast.length === 0) {
                    Swal.fire({
                        icon: 'error',
                        title: 'Data Kosong',
                        text: 'Tidak ada data untuk kombinasi ini.'
                    });
                    return;
                }

                var tbody = '';

                $.each(response.forecast, function(i, row) {
                    var bulanInput = $('#pilihBulan').val();

                    var dateObj = new Date(row.bulan);
                    var monthNumber = dateObj.getMonth() + 1;

                    if (bulanInput !== "all" && monthNumber != bulanInput) {
                        return;
                    }

                    var valPrediksi = parseFloat(row.eksemplar);
                    var valAktual = parseFloat(row.aktual_lalu || 0);
                    var maeBulan = parseFloat(row.mae_spesifik || 0);

                    // Hitung Error Persen = MAE / Prediksi × 100%
                    var errorPersen = 0;
                    if (valPrediksi > 0) {
                        errorPersen = (maeBulan / valPrediksi) * 100;
                    }

                    var batasBawah = Math.max(0, Math.round(valPrediksi - maeBulan));
                    var batasAtas = Math.round(valPrediksi + maeBulan);

                    var trendIcon = '';
                    if (valPrediksi > valAktual) trendIcon = '<i class="fas fa-arrow-up text-success ml-2"></i>';
                    else if (valPrediksi < valAktual && valAktual > 0) trendIcon = '<i class="fas fa-arrow-down text-danger ml-2"></i>';

                    // Warna badge Error Persen berdasarkan tingkat error
                    var errorClass = 'success';
                    if (errorPersen > 20) errorClass = 'danger';
                    else if (errorPersen > 10) errorClass = 'warning';

                    tbody += `
                        <tr>
                            <td>${kategori}</td>
                            <td class="text-center font-weight-bold">${row.bulan}</td>
                            <td class="text-right font-weight-bold text-dark">
                                ${valPrediksi.toLocaleString('id-ID')} ${trendIcon}
                            </td>
                            <td class="text-right text-danger font-weight-bold">
                                ± ${maeBulan.toLocaleString('id-ID')}
                            </td>
                            <td class="text-right">
                                <span class="badge badge-${errorClass}" style="font-size:0.85em">
                                    ${errorPersen.toFixed(2)}%
                                </span>
                            </td>
                            <td class="text-center">
                                <span class="badge badge-info" style="font-size:0.9em">
                                    ${batasBawah.toLocaleString('id-ID')} - ${batasAtas.toLocaleString('id-ID')}
                                </span>
                            </td>
                        </tr>`;
                });

                $('#tabelPrediksi tbody').html(tbody);
                $('#cardHasil').fadeIn();

                renderChart(response);
            },
            error: function(xhr) {
                Swal.close();
                Swal.fire({
                    icon: 'error',
                    title: 'Gagal Terhubung',
                    text: 'Pastikan server Flask sudah jalan di port 5000'
                });
            }
        });
    });

    function renderChart(response) {
        $('#cardGrafik').fadeIn();
        const ctx = document.getElementById('chartPrediksi').getContext('2d');
        let labels = [];
        let dataHistory = [];
        let dataForecast = [];

        response.history.forEach(item => {
            labels.push(item.bulan);
            dataHistory.push(item.eksemplar);
            dataForecast.push(null);
        });
        if (dataHistory.length > 0) dataForecast[dataForecast.length - 1] = dataHistory[dataHistory.length - 1];
        response.forecast.forEach(item => {
            labels.push(item.bulan);
            dataForecast.push(item.eksemplar);
        });

        if (salesChart) salesChart.destroy();
        salesChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                        label: 'History',
                        data: dataHistory,
                        borderColor: '#4e73df',
                        fill: false
                    },
                    {
                        label: 'Prediksi',
                        data: dataForecast,
                        borderColor: '#e74a3b',
                        borderDash: [5, 5],
                        fill: false
                    }
                ]
            },
            options: {
                maintainAspectRatio: false
            }
        });
    }
</script>