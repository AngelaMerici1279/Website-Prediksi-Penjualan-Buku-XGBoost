<?php
defined('BASEPATH') OR exit('No direct script access allowed');
class Auth_model extends CI_Model {

    public function __construct() {
        parent::__construct();
        $this->load->database();
    }
   // Fungsi untuk mendapatkan data user berdasarkan username
    public function getUser($username) {
        return $this->db->get_where('pegawai', ['username' => $username])->row_array();
    }

    // Fungsi untuk memverifikasi login dan mendapatkan role
    public function verifyLogin($username, $password) {
        
        $user = $this->getUser($username);
        $password = md5($password);
        $kueri = "SELECT * FROM pegawai WHERE username = '$username' AND password = '$password'";
        $user = $this->db->query($kueri)->row_array();
        
        if ($user && $user['password'] == $password) {
            return $user; // Mengembalikan data user (termasuk role)
        }
        
        return false; // Login gagal
    }
}