import pandas as pd             
        
def get_1am_price_results(df):
    return (df
            .assign(bookr_1=-1,
                    exr_1=-1)
            .assign(bookr_1=lambda x : x.bookr_1.where(x.WIN_LOSE != 1, x['1_mean_book_NR']-1),
                    exr_1=lambda x : x.exr_1.where(x.WIN_LOSE != 1, (x['1_ex_NR']-1)*.98)))


def get_6am_price_results(df):
    return (df
            .assign(bookr_6=-1,
                    exr_6=-1)
            .assign(bookr_6=lambda x : x.bookr_6.where(x.WIN_LOSE != 1, x['6_mean_book_NR']-1),
                    exr_6=lambda x : x.exr_6.where(x.WIN_LOSE != 1, (x['6_ex_NR']-1)*.98)))


def get_10am_price_results(df):
    return (df
            .assign(bookr_10=-1,
                    exr_10=-1)
            .assign(bookr_10=lambda x : x.bookr_10.where(x.WIN_LOSE != 1, x['10_mean_book_NR']-1),
                    exr_10=lambda x : x.exr_10.where(x.WIN_LOSE != 1, (x['10_ex_NR']-1)*.98)))


def get_bsp_price_results(df):
    return (df
            .assign(bspr=-1,
                    bsp_ncr=-1)
            .assign(bspr=lambda x : x.bspr.where(x.WIN_LOSE != 1, (x['BSP']-1)*.98),
                    bsp_ncr=lambda x : x.bsp_ncr.where(x.WIN_LOSE != 1, x['BSP']-1)))


def get_isp_price_results(df):
    return (df
            .assign(ispr=-1)
            .assign(ispr=lambda x : x.ispr.where(x.WIN_LOSE != 1, x['isp']-1)))


def get_results(df):
    return (get_1am_price_results(df)
            .pipe(get_6am_price_results)
            .pipe(get_10am_price_results)
            .pipe(get_bsp_price_results)
            .pipe(get_isp_price_results))
