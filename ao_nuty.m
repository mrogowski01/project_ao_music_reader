function crd=ao_nuty(file)
    im = double(rgb2gray(imread(file))/255);
%     figure
%     imshow(im)
    bin = imbinarize(im);

    bin = imclose(bin, ones(2));
    bin = imopen(bin, ones(8));
    bin = imdilate(bin, ones(3));
    bin=~bin;

    l = bwlabel(bin);

    fun = {@AO5RMalinowska, @AO5RHaralick, @AO5RDanielsson}; % tablica "wskaznikow" do funkcji

    l=filter(l, 0.3, fun);

    a=regionprops(l>0, 'Centroid');
    crd=zeros(length(a), 2);

    for i=1:length(a)
        crd(i, :) = a(i).Centroid;
    end
end


function img = filter(l, wsp, fun)
    %%%%%%%%%%
    a=regionprops(l>0, 'all');
    cir = zeros(length(a), length(fun));
    
    for i=1:length(a)
        tmp=a(i).Image;
        for j=1:length(fun)
            cir(i,j) = fun{j}(tmp);
        end
    end
    %%%%%%%%%


    m = mean(cir);
    s = std(cir);

    odch = abs((cir-m)./s);

    for i=1:length(odch)
        if odch(i, :)>wsp | a(i).Area < 5
            l(l==i) = 0;
        end
    end

    img = l;
end
