# Contents of ~/my_app/pages/page_3.py
import streamlit as st
import scanpy as sc
import matplotlib.pyplot as plt
import io
import base64
import pandas as pd


##############################################################################################################
def image_to_button(image,name,format):
            img = io.BytesIO()
            image.savefig(img, format=format,dpi=300,bbox_inches='tight')
            img.seek(0)
            b64 = base64.b64encode(img.read()).decode()
            htm = f'<a href="data:file/txt;base64,{b64}" download="{name}"><input type="button" value="Download Image"></a>'
            return htm

st.set_page_config(layout="wide")
st.set_option('deprecation.showPyplotGlobalUse', False)
sc.set_figure_params(dpi=300)

@st.cache_resource
def upload_sc(adata):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return sc.read_h5ad(adata)
##############################################################################################################
st.write('## scRNA-vis')
st.write("Webapp for visualization of ccRCC single cell transcripts. Created by **Sergio Hernández** 🧬")
st.sidebar.divider()
colormap= st.sidebar.radio("UMAP Colormap",("magma","Reds","hot","rainbow","turbo","Spectral"),horizontal=True)
st.sidebar.divider()
saveas = st.sidebar.radio("Save as",("png","svg"),horizontal=True)

f_adata_upload = st.file_uploader("Upload your Dataset",type="h5ad")
if f_adata_upload is not None:
    with st.form("my_form"):
        f_adata = upload_sc(f_adata_upload)

        options = st.sidebar.multiselect("Select Genes",f_adata.raw.var_names.tolist())
        submitted = st.form_submit_button("Run")
        if submitted:
                st.subheader("Selected Genes")
                sg = sc.pl.umap(f_adata,color=options,use_raw=True,cmap=colormap,return_fig=True)
                st.pyplot(sg)
                if saveas == "png":
                    st.markdown(image_to_button(sg,f"{options}.png",saveas),unsafe_allow_html=True)
                else: 
                    st.markdown(image_to_button(sg,f"{options}.svg",saveas),unsafe_allow_html=True)
                st.divider()

                 

     



