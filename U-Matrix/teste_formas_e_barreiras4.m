close all
path(path,'C:\Users\rapha\Desktop\U_Matrix\')  
addpath(genpath('SOM-Toolbox-master'));
figure(4)
clf
msize=[50 50]; % quantidade de neurÃ´nios (linha x coluna)
%  strDados={'dfm_nilceu_216';'ediferencial_k216';'ediferencial_N5_k216';...
%      'ediferencial_N100_k216';'ediscreta_k216';'ediscreta_N50_k216';...
%      'ediscreta_N1000_k216';'ediscreta_numbis500_k216';...
%      'ediscreta_numbis5000_k216';'dfm_nilceu_216';'nmbe_k216';...
%      'ereny_k216_a05';'ereny_k216_a10';'ereny_k216_a25';...
%      'ereny_k216_a50';'ereny_k216_a100'};
%strDados={'shapeCN_silhouette_0'};
strDados={'describe2'};

%carrega dum arquivo que tem a cor das formas da primeira classe na 
%primeira linha e assim por diante 
cores= load(strcat('cores_med117.txt'),'-ascii');

for l=1:size(strDados,1)
    strFig=strDados{l,1};
    data = load(strcat(strFig,'.txt'),'-ascii');
    sz = size(data);
    dd = data(:,2:sz(2));
    %dd = load('saida.txt','-ascii')
    sz = size(dd);
    SD = som_data_struct(dd,'name','Falhas');
    SD = som_normalize(SD,'var');
    
    % adiciona rórulos
    % adiciona rótulos
    for k=1:length(ss)
        SD = som_label(SD,'add',k,ss{k});
    end
    
    % inicializa a rede SOM
    SM = som_make(SD,'msize',msize);
    SM= som_autolabel(SM,SD,'vote');
    som_show(SM,'umat','all');%,'comp',[1:3],'norm','d','bar','none','colormap',hot,'subplots',[3 3]);
    
    %
    
    figure(2);
    clf;
    h=som_show(SM,'umat',{'',''},'footnote','');%,'comp',[1:3],'norm','d','bar','none','colormap',hot,'subplots',[3 3]);
    set(h.colorbar,'FontSize',20);
    hold on;
    FS=22;
    [sgrid,m,l,t,s]=som_grid(SM,'lattice','hexa','Label',SM.labels,'LabelSize',FS,'LabelColor',[0.9 0.9 0.9],'Marker','none','Line','none');
    colormap(gray);
    colormap(flipud(colormap));
    %saveas(gcf,strcat('analisefalha_cba_matrizu_',strFig),'png');
    
    %%
    clear p;
    for k=1:length(t)
        p(k,:)=get(t(k),'Position');
        delete(t(k));
    end
    %%
    %imshow(uint8(zeros(uint8(max(p(:,1)+2)),uint8(max(p(:,2)+2)))));
    set(gca,'XLim',[-1 max(p(:,1))+1]);
    set(gca,'YLim',[-1 max(p(:,2))+1]);
    cla=data(1:end,1);
    fator=2;
    for k=1:size(p,1)
        s=SM.labels{k};
        %s=data(k,1);
        if length(s)>0
            %l->escolhe a figura
            l=(s(1)-65)*tamdados(2)+str2num(s(4:end-1));
            %g->escolhe a cor
            aux=data(l,1)==cla;
            %g=(data(l,1)*300-64)*(sum(cla)+1);
            %g=(s(1)-64)*(tamdados(1)+1);
            IMG=M(:,:,1,l);
            %IMG=imresize(IMG,5);
            %CON=1-(-IMG+imdilate(IMG,strel('disk',2)));
            
%             image([p(k,1)-1 p(k,1)+1],[p(k,2)-1 p(k,2)+1],uint8(~IMG*(data(l,1))*255/32),'AlphaData',~IMG);
%             %image([p(k,1)-1 p(k,1)+1],[p(k,2)-1 p(k,2)+1],uint8(~IMG*g),'AlphaData',~IMG);
%             image([p(k,1)-1 p(k,1)+1],[p(k,2)-1 p(k,2)+1],~CON,'AlphaData',~CON);
            xi=(p(k,1)-fator);
            xf=(p(k,1)+fator);
            yi=(p(k,2)-fator);
            yf=(p(k,2)+fator);
            
            im=image([xi xf],[yi yf],uint8(~IMG*(data(l,1))*255/32),'AlphaData',~IMG);
%            set(im,'CData',double(cat(3, (cores(data(l,1)+1,1)/255).*(~IMG),...
%                (cores(data(l,1)+1,2)/255).*(~IMG),(cores(data(l,1)+1,3)/255).*(~IMG))));
            set(im,'CData',double(cat(3, (cores(data(l,1),1)/255).*(~IMG),...
                (cores(data(l,1),2)/255).*(~IMG),(cores(data(l,1),3)/255).*(~IMG))));
            get(im,'CData');
            %image([p(k,1)-1 p(k,1)+1],[p(k,2)-1 p(k,2)+1],uint8(~IMG*g),'AlphaData',~IMG);
            %image([xi xf],[yi yf],~CON*255,'AlphaData',~CON);
            %image([xi xf],[yi yf],~CON,'AlphaData',~CON);
            %g
        end
    end
    %colormap([[1 1 1]; colorcube(tamdados(1)*110); [0 0 0]]);
    %colormap([[1 1 1]; lines(tamdados(1)*15); [0 0 0]])
    %colormap([[1 1 1]; hsv(tamdados(1)*15); [0 0 0]])
    %colormap([[1 1 1]; jet(tamdados(1)*15); [0 0 0]])
    %colormap([[1 1 1]; hot(tamdados(1)*15); [0 0 0]])
    colorbar off;
    
    %end
    
    %saveas(gcf,strcat(strFig,'_formas'),'fig');
end