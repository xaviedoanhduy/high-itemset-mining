import multiprocessing as mp
import time



class GiaiThuaSongSong:
        def __init__(self,number):
                self.number = number
                self.result_list = []

        def DoiSangChuoi(self,n):
                s = ''
                while n > 1000:
                        s = '.' + str(n % 1000).rjust(3, '0') + s
                        n //= 1000
                s = str(n % 1000) + s
                n //= 1000
                return s

        def pGiaiThua(self, ib, ie):
            s = 1
            for i in range(ib, ie+1):
                s *= i
            return s

        def log_result(self, result):
            # Hàm được gọi bất kỳ khi nào pGiaiThua(ib, ie) trả ra kết quả.
            # result_list được thực hiện trên main process, khong phải pool workers.
            self.result_list.append(result)

        def apply_async_with_callback(self):
            iCPU = mp.cpu_count()
            pool = mp.Pool(processes=iCPU)
            n = N//(iCPU)
            print('n= ',n)
            ib = 1; ie = n
            for i in range(iCPU-1):
                pool.apply_async(self.pGiaiThua, args=(ib, ie), callback = self.log_result)
                ib += n
                ie += n
            pool.apply_async(self.pGiaiThua, args=(ib, N), callback = self.log_result)
            pool.close()
            pool.join()
            #print(result_list)

        def Product(self):
            s = 1
            for re in self.result_list:
                s*=re
            return s


if __name__ == '__main__':
        N = 100
        print("GiaiThua(%d)!" % N,end='\t')
        print('Số CPU: ',mp.cpu_count())
        t0 = time.time()
        obj = GiaiThuaSongSong(N)
        obj.apply_async_with_callback()
        kq = obj.Product()
        print("Song song: Thời gian %8.6f giây" %(time.time()-t0))
        print("GiaiThua(%d)! là %s" % (N, obj.DoiSangChuoi( kq )))
#==================================================

        
