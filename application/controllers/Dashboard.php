<?php
defined('BASEPATH') or exit('No direct script access allowed');

class dashboard extends CI_Controller
{

    public function __construct()
    {
        parent::__construct();
        // Cek apakah user sudah login
        if (!$this->session->userdata('username')) {
            redirect('auth/login');  // Jika belum login, redirect ke halaman login
        }
    }

    // Halaman Dashboard Kepegawaian
    public function kepegawaian()
    {
        if ($this->session->userdata('role') != '1' && $this->session->userdata('role') != '8') {
            redirect('auth/login'); // Jika role bukan kepegawaian, redirect ke login
        }

        $this->load->model('Pegawai_Model');
        $data['chartStatus'] = $this->Pegawai_Model->dataGrafik();
        $data['roleBar'] = $this->Pegawai_Model->get_pegawai_by_role();
        $data['areaChartHireDate'] = $this->Pegawai_Model->dataTanggalMasuk();
        $data['Kepegawaian'] = $this->Pegawai_Model->getJumlahPegawai(1);
        $data['Penjualan'] = $this->Pegawai_Model->getJumlahPegawai(2);
        $data['Pemasaran'] = $this->Pegawai_Model->getJumlahPegawai(3);
        $data['Penerbitan'] = $this->Pegawai_Model->getJumlahPegawai(4);
        $data['Pembelian'] = $this->Pegawai_Model->getJumlahPegawai(5);
        $data['Programmer'] = $this->Pegawai_Model->getJumlahPegawai(6);
        $data['Percetakan'] = $this->Pegawai_Model->getJumlahPegawai(7);

        $this->load->view('grafikKepegawaian', $data);
        // $this->load->view('dashboard/dashboardk', $data);
    }

    // Halaman Dashboard Penjualan
    public function penjualan()
    {
        if ($this->session->userdata('role') != '2') {
            redirect('auth/login'); // Jika role bukan penjualan, redirect ke login
        }
        $this->load->view('headerdashboard/headerPenjualan');
        $this->load->view('dashboard/dashboardp');
    }
}
