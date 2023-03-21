function h = ao_pieciolinia(file)
    im = double(rgb2gray(imread(file)))/255;
    bin = imbinarize(im);
    mask = [0 1 0; 0 0 0; 0 1 0];
    mask2 = zeros(21);
    mask2(10, :) = 1;
    
    tmp = imdilate(bin, mask);
    tmp = imerode(tmp, ones(3));
    tmp = bin|~tmp;
    
    tmp = ~tmp;
    
    a = regionprops(tmp, 'Area');
    l = bwlabel(tmp);
    for i=1:length(a)
        if a(i).Area < 10
            l(l==i) = 0;
        end
    end
    tmp = l>0;
    
    tmp = tmp | tmp(:, end:-1:1);
    tmp = imdilate(tmp, mask2);
    
    a = regionprops(tmp, 'MajorAxisLength');
    l = bwlabel(tmp);
    for i=1:length(a)
        if a(i).MajorAxisLength < 200
            l(l==i) = 0;
        end
    end

%     bin = bwmorph(l>0, 'thin');
%     bin = imclose(bin, ones(7));
    length_mask = zeros(101);
    length_mask(51,:) = ones(1,101);
    bin = imdilate(l>0, length_mask);
    bin = imdilate(bin, length_mask);

    a = regionprops(bin, 'Centroid');
    h = zeros(1,length(a));
    for i=1:length(a)
        h(i)=a(i).Centroid(2);
    end
end